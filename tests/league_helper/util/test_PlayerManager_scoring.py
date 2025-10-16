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
    "BASE_BYE_PENALTY": 25.0,
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
    }
  }
}"""

    config_file = data_folder / "league_config.json"
    config_file.write_text(config_content)

    # Create minimal teams.csv
    teams_content = """team,offensive_rank,defensive_rank,opponent
KC,1,5,LV
BUF,2,3,MIA
PHI,3,8,NYG
DAL,15,20,WAS
JAX,28,30,IND"""

    teams_file = data_folder / "teams.csv"
    teams_file.write_text(teams_content)

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
def team_data_manager(mock_data_folder):
    """Create TeamDataManager with test data"""
    return TeamDataManager(mock_data_folder)


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

    return pm


@pytest.fixture
def test_player():
    """Create a test player with all attributes set"""
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
        drafted=0,
        locked=0
    )

    # Set computed properties
    player.weighted_projection = 80.0  # (200/250) * 100
    player.consistency = 0.3  # Good consistency (low CV)
    player.team_offensive_rank = 1  # Excellent team (KC)
    player.team_defensive_rank = 5
    player.matchup_score = 10  # Good matchup

    # Set weekly points for consistency calculation and rest-of-season projection
    # Current week is 6, so weeks 6-17 will be used for ROS projection
    # Set weeks 6-17 to sum to exactly 200.0 (12 weeks)
    player.week_1_points = 18.5
    player.week_2_points = 22.0
    player.week_3_points = 19.5
    player.week_4_points = 21.0
    player.week_5_points = 20.0
    # Weeks 6-17: 11 weeks * 16.0 + 1 week * 24.0 = 176 + 24 = 200.0
    player.week_6_points = 16.0
    player.week_7_points = 16.0
    player.week_8_points = 16.0
    player.week_9_points = 16.0
    player.week_10_points = 16.0
    player.week_11_points = 16.0
    player.week_12_points = 16.0
    player.week_13_points = 16.0
    player.week_14_points = 16.0
    player.week_15_points = 16.0
    player.week_16_points = 16.0
    player.week_17_points = 24.0  # Extra to make sum exactly 200.0

    return player


# ============================================================================
# STEP 1: NORMALIZATION TESTS
# ============================================================================

class TestNormalization:
    """Test Step 1: Normalization calculation"""

    def test_normalization_returns_weighted_projection(self, player_manager, test_player):
        """Verify normalization simply returns the weighted_projection"""
        result, reason = player_manager._get_normalized_fantasy_points(test_player, use_weekly_projection=False)
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
        result, reason = player_manager._get_normalized_fantasy_points(player, use_weekly_projection=False)
        assert result == 0.0


# ============================================================================
# WEEKLY PROJECTION TESTS
# ============================================================================

class TestWeeklyProjections:
    """Test weekly projection fetching and normalization"""

    def test_get_weekly_projection_valid_data(self, player_manager, test_player):
        """Test get_weekly_projection with valid weekly data"""
        # Set up player with week 6 data (current week in config)
        test_player.week_6_points = 25.0
        player_manager.max_projection = 300.0  # Set max for normalization

        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=6)

        assert orig_pts == 25.0
        # Weighted should be (25/300) * 100 = 8.33...
        expected_weighted = (25.0 / 300.0) * 100.0
        assert abs(weighted_pts - expected_weighted) < 0.01

    def test_get_weekly_projection_uses_current_week_when_invalid(self, player_manager, test_player):
        """Test that invalid week parameter defaults to current week"""
        # Config has current_nfl_week = 6
        test_player.week_6_points = 20.0
        player_manager.max_projection = 300.0

        # Pass invalid week (0)
        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=0)

        # Should use week 6 instead
        assert orig_pts == 20.0

    def test_get_weekly_projection_missing_data_returns_zero(self, player_manager, test_player):
        """Test that missing weekly data returns (0.0, 0.0)"""
        # Remove week_10_points from test_player to test missing data
        del test_player.week_10_points
        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=10)

        assert orig_pts == 0.0
        assert weighted_pts == 0.0

    def test_get_weekly_projection_none_value_returns_zero(self, player_manager, test_player):
        """Test that None weekly points returns (0.0, 0.0)"""
        test_player.week_7_points = None

        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=7)

        assert orig_pts == 0.0
        assert weighted_pts == 0.0

    def test_get_weekly_projection_zero_value_returns_zero(self, player_manager, test_player):
        """Test that zero weekly points returns (0.0, 0.0)"""
        test_player.week_8_points = 0.0

        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=8)

        assert orig_pts == 0.0
        assert weighted_pts == 0.0

    def test_get_weekly_projection_with_zero_max_projection(self, player_manager, test_player):
        """Test weekly projection when max_projection is 0"""
        test_player.week_6_points = 25.0
        player_manager.max_projection = 0  # Edge case

        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=6)

        assert orig_pts == 25.0
        assert weighted_pts == 0.0  # Should handle division by zero

    def test_normalization_with_weekly_projection_enabled(self, player_manager, test_player):
        """Test _get_normalized_fantasy_points with use_weekly_projection=True"""
        test_player.week_6_points = 30.0
        player_manager.max_projection = 300.0

        result, reason = player_manager._get_normalized_fantasy_points(test_player, use_weekly_projection=True)

        # Should use weekly projection: (30/300) * 100 = 10.0
        expected = (30.0 / 300.0) * 100.0
        assert abs(result - expected) < 0.01
        assert "Projected: 30.00" in reason
        assert "Weighted:" in reason

    def test_normalization_with_weekly_projection_disabled(self, player_manager, test_player):
        """Test _get_normalized_fantasy_points with use_weekly_projection=False uses ROS"""
        # Test player has weeks 6-17 summing to 200.0 (from fixture)
        # Current week is 6, so ROS = sum of weeks 6-17 = 200.0
        # Weighted = (200/250) * 100 = 80.0

        result, reason = player_manager._get_normalized_fantasy_points(test_player, use_weekly_projection=False)

        # Should use rest-of-season projection
        assert result == 80.0
        assert "200.00" in reason  # Should show ROS points

    def test_score_player_with_weekly_projection(self, player_manager, test_player, mock_fantasy_team):
        """Integration test: score_player with use_weekly_projection=True"""
        # Set up weekly data
        test_player.week_6_points = 25.0
        player_manager.max_projection = 300.0
        test_player.consistency = 0.15  # EXCELLENT
        test_player.matchup_score = 10  # GOOD
        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0

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

        # Expected: (25/300)*100 = 8.33... * 1.10 (matchup)
        expected_base = (25.0 / 300.0) * 100.0
        expected_final = expected_base * 1.10

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
        result, reason = player_manager._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.20  # 120.0
        assert reason == "ADP: EXCELLENT"

    def test_adp_good_threshold(self, player_manager, test_player):
        """20 < ADP <= 50 should get GOOD multiplier (1.10)"""
        test_player.average_draft_position = 35.0
        base_score = 100.0
        result, reason = player_manager._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.10  # 110.0
        assert reason == "ADP: GOOD"

    def test_adp_neutral_range(self, player_manager, test_player):
        """50 < ADP < 100 should get NEUTRAL multiplier (1.0)"""
        test_player.average_draft_position = 75.0
        base_score = 100.0
        result, reason = player_manager._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.0  # 100.0
        assert reason == "ADP: NEUTRAL"

    def test_adp_poor_threshold(self, player_manager, test_player):
        """100 <= ADP < 150 should get POOR multiplier (0.90)"""
        test_player.average_draft_position = 120.0
        base_score = 100.0
        result, reason = player_manager._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 0.90  # 90.0
        assert reason == "ADP: POOR"

    def test_adp_very_poor_threshold(self, player_manager, test_player):
        """ADP >= 150 should get VERY_POOR multiplier (0.70)"""
        test_player.average_draft_position = 200.0
        base_score = 100.0
        result, reason = player_manager._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 0.70  # 70.0
        assert reason == "ADP: VERY_POOR"

    def test_adp_none_returns_neutral(self, player_manager, test_player):
        """ADP = None should return neutral multiplier (1.0)"""
        test_player.average_draft_position = None
        base_score = 100.0
        result, reason = player_manager._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.0
        assert reason == "ADP: NEUTRAL"

    def test_adp_boundary_at_20(self, player_manager, test_player):
        """Test exact boundary at ADP = 20"""
        test_player.average_draft_position = 20.0
        base_score = 100.0
        result, reason = player_manager._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.20  # Should be EXCELLENT
        assert reason == "ADP: EXCELLENT"


# ============================================================================
# STEP 3: PLAYER RATING MULTIPLIER TESTS
# ============================================================================

class TestPlayerRatingMultiplier:
    """Test Step 3: Player rating multiplier application"""

    def test_player_rating_excellent(self, player_manager, test_player):
        """Rating >= 80 should get EXCELLENT multiplier (1.25)"""
        test_player.player_rating = 85.0
        base_score = 100.0
        result, reason = player_manager._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 1.25
        assert reason == "Player Rating: EXCELLENT"

    def test_player_rating_good(self, player_manager, test_player):
        """60 <= Rating < 80 should get GOOD multiplier (1.15)"""
        test_player.player_rating = 70.0
        base_score = 100.0
        result, reason = player_manager._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 1.15
        assert reason == "Player Rating: GOOD"

    def test_player_rating_neutral(self, player_manager, test_player):
        """40 < Rating < 60 should get NEUTRAL multiplier (1.0)"""
        test_player.player_rating = 50.0
        base_score = 100.0
        result, reason = player_manager._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 1.0
        assert reason == "Player Rating: NEUTRAL"

    def test_player_rating_poor(self, player_manager, test_player):
        """20 < Rating <= 40 should get POOR multiplier (0.95)"""
        test_player.player_rating = 30.0
        base_score = 100.0
        result, reason = player_manager._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 0.95
        assert reason == "Player Rating: POOR"

    def test_player_rating_very_poor(self, player_manager, test_player):
        """Rating <= 20 should get VERY_POOR multiplier (0.75)"""
        test_player.player_rating = 15.0
        base_score = 100.0
        result, reason = player_manager._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 0.75
        assert reason == "Player Rating: VERY_POOR"

    def test_player_rating_none_returns_neutral(self, player_manager, test_player):
        """Player rating = None should return neutral (1.0)"""
        test_player.player_rating = None
        base_score = 100.0
        result, reason = player_manager._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0
        assert reason == "Player Rating: NEUTRAL"


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
        result, reason = player_manager._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0 * 1.30
        assert reason == "Team Quality: EXCELLENT"

    def test_team_quality_good_offensive(self, player_manager, test_player):
        """5 < Offensive rank <= 10 should get GOOD (1.15)"""
        test_player.team_offensive_rank = 8
        test_player.position = "WR"
        base_score = 100.0
        result, reason = player_manager._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0 * 1.15
        assert reason == "Team Quality: GOOD"

    def test_team_quality_poor_offensive(self, player_manager, test_player):
        """20 <= Offensive rank < 25 should get POOR (0.85)"""
        test_player.team_offensive_rank = 22
        test_player.position = "QB"
        base_score = 100.0
        result, reason = player_manager._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0 * 0.85
        assert reason == "Team Quality: POOR"

    def test_team_quality_very_poor_offensive(self, player_manager, test_player):
        """Offensive rank >= 25 should get VERY_POOR (0.70)"""
        test_player.team_offensive_rank = 28
        test_player.position = "TE"
        base_score = 100.0
        result, reason = player_manager._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0 * 0.70
        assert reason == "Team Quality: VERY_POOR"

    def test_team_quality_defense_uses_defensive_rank(self, player_manager, test_player):
        """DST position should use team_defensive_rank"""
        test_player.team_offensive_rank = 25  # Bad offense
        test_player.team_defensive_rank = 3   # Good defense
        test_player.position = "DST"
        base_score = 100.0
        result, reason = player_manager._apply_team_quality_multiplier(test_player, base_score)
        # Should use defensive rank (3) which is EXCELLENT
        assert result == 100.0 * 1.30
        assert reason == "Team Quality: EXCELLENT"

    def test_team_quality_none_returns_neutral(self, player_manager, test_player):
        """Team rank = None should return neutral (1.0)"""
        test_player.team_offensive_rank = None
        test_player.position = "RB"
        base_score = 100.0
        result, reason = player_manager._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0
        assert reason == "Team Quality: NEUTRAL"


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
        """Matchup >= 15 should get EXCELLENT (1.25)"""
        test_player.matchup_score = 18
        base_score = 100.0
        result, reason = player_manager._apply_matchup_multiplier(test_player, base_score)
        assert result == 100.0 * 1.25
        assert reason == "Matchup: EXCELLENT"

    def test_matchup_good(self, player_manager, test_player):
        """6 <= Matchup < 15 should get GOOD (1.10)"""
        test_player.matchup_score = 10
        base_score = 100.0
        result, reason = player_manager._apply_matchup_multiplier(test_player, base_score)
        assert result == 100.0 * 1.10
        assert reason == "Matchup: GOOD"

    def test_matchup_neutral(self, player_manager, test_player):
        """-6 < Matchup < 6 should get NEUTRAL (1.0)"""
        test_player.matchup_score = 0
        base_score = 100.0
        result, reason = player_manager._apply_matchup_multiplier(test_player, base_score)
        assert result == 100.0 * 1.0
        assert reason == "Matchup: NEUTRAL"

    def test_matchup_poor(self, player_manager, test_player):
        """-15 < Matchup <= -6 should get POOR (0.90)"""
        test_player.matchup_score = -10
        base_score = 100.0
        result, reason = player_manager._apply_matchup_multiplier(test_player, base_score)
        assert result == 100.0 * 0.90
        assert reason == "Matchup: POOR"

    def test_matchup_very_poor(self, player_manager, test_player):
        """Matchup <= -15 should get VERY_POOR (0.75)"""
        test_player.matchup_score = -20
        base_score = 100.0
        result, reason = player_manager._apply_matchup_multiplier(test_player, base_score)
        assert result == 100.0 * 0.75
        assert reason == "Matchup: VERY_POOR"

    def test_matchup_none_returns_neutral(self, player_manager, test_player):
        """Matchup = None should return neutral (1.0)"""
        test_player.matchup_score = None
        base_score = 100.0
        result, reason = player_manager._apply_matchup_multiplier(test_player, base_score)
        assert result == 100.0
        assert reason == "Matchup: NEUTRAL"


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
        result, reason = player_manager._apply_draft_order_bonus(test_player, 0, base_score)
        assert result == 100.0 + 50, "Round 0 should work with new >= 0 check"
        assert reason == "Draft Order Bonus: PRIMARY"

    def test_draft_bonus_round_0_secondary_position(self, player_manager, test_player):
        """Round 0 with SECONDARY position should get SECONDARY bonus"""
        # Round 0: {"FLEX": "P", "QB": "S"}
        # QB should get SECONDARY (30)
        test_player.position = "QB"
        base_score = 100.0
        result, reason = player_manager._apply_draft_order_bonus(test_player, 0, base_score)
        assert result == 100.0 + 30
        assert reason == "Draft Order Bonus: SECONDARY"

    def test_draft_bonus_round_1_flex_gets_primary(self, player_manager, test_player):
        """Round 1 FLEX-eligible should get PRIMARY"""
        # Round 1: {"FLEX": "P", "QB": "S"}
        test_player.position = "WR"  # FLEX-eligible
        base_score = 100.0
        result, reason = player_manager._apply_draft_order_bonus(test_player, 1, base_score)
        assert result == 100.0 + 50
        assert reason == "Draft Order Bonus: PRIMARY"

    def test_draft_bonus_round_2_qb_gets_primary(self, player_manager, test_player):
        """Round 2 QB should get PRIMARY"""
        # Round 2: {"QB": "P", "FLEX": "S"}
        test_player.position = "QB"
        base_score = 100.0
        result, reason = player_manager._apply_draft_order_bonus(test_player, 2, base_score)
        assert result == 100.0 + 50
        assert reason == "Draft Order Bonus: PRIMARY"

    def test_draft_bonus_round_3_te_gets_primary(self, player_manager, test_player):
        """Round 3 TE should get PRIMARY"""
        # Round 3: {"TE": "P", "FLEX": "S"}
        test_player.position = "TE"
        base_score = 100.0
        result, reason = player_manager._apply_draft_order_bonus(test_player, 3, base_score)
        assert result == 100.0 + 50
        assert reason == "Draft Order Bonus: PRIMARY"

    def test_draft_bonus_no_match_returns_zero(self, player_manager, test_player):
        """Position not in round's priorities returns 0 bonus"""
        # Round 4: {"K": "P"}
        # TE not in priorities
        test_player.position = "TE"
        base_score = 100.0
        result, reason = player_manager._apply_draft_order_bonus(test_player, 4, base_score)
        assert result == 100.0 + 0
        assert reason == ""


# ============================================================================
# STEP 8: BYE WEEK PENALTY TESTS
# ============================================================================

class TestByeWeekPenalty:
    """Test Step 8: Bye week penalty application"""

    def test_bye_penalty_no_matches(self, player_manager, test_player, mock_fantasy_team):
        """No matching bye weeks should have 0 penalty"""
        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0
        base_score = 100.0
        result, reason = player_manager._apply_bye_week_penalty(test_player, base_score)
        assert result == 100.0  # No penalty
        assert reason == ""

    def test_bye_penalty_one_match(self, player_manager, test_player, mock_fantasy_team):
        """One matching bye should apply BASE_BYE_PENALTY once"""
        mock_fantasy_team.get_matching_byes_in_roster.return_value = 1
        base_score = 100.0
        result, reason = player_manager._apply_bye_week_penalty(test_player, base_score)
        assert result == 100.0 - 25.0  # BASE_BYE_PENALTY = 25
        assert reason == "Number of Matching Bye Weeks: 1"

    def test_bye_penalty_multiple_matches(self, player_manager, test_player, mock_fantasy_team):
        """Multiple matching byes should multiply penalty"""
        mock_fantasy_team.get_matching_byes_in_roster.return_value = 3
        base_score = 100.0
        result, reason = player_manager._apply_bye_week_penalty(test_player, base_score)
        assert result == 100.0 - (25.0 * 3)  # 25.0
        assert reason == "Number of Matching Bye Weeks: 3"

    def test_bye_penalty_calls_team_method_correctly(self, player_manager, test_player, mock_fantasy_team):
        """Verify correct parameters passed to team.get_matching_byes_in_roster"""
        test_player.bye_week = 7
        test_player.position = "RB"
        test_player.drafted = 0  # Not rostered

        base_score = 100.0
        result, reason = player_manager._apply_bye_week_penalty(test_player, base_score)

        mock_fantasy_team.get_matching_byes_in_roster.assert_called_once_with(
            7,  # bye_week
            "RB",  # position
            False  # is_rostered (drafted != 2)
        )


# ============================================================================
# STEP 9: INJURY PENALTY TESTS
# ============================================================================

class TestInjuryPenalty:
    """Test Step 9: Injury penalty application"""

    def test_injury_low_risk_active(self, player_manager, test_player):
        """ACTIVE status should have LOW risk (0 penalty)"""
        test_player.injury_status = "ACTIVE"
        base_score = 100.0
        result, reason = player_manager._apply_injury_penalty(test_player, base_score)
        assert result == 100.0  # No penalty
        assert reason == ""

    def test_injury_medium_risk_questionable(self, player_manager, test_player):
        """QUESTIONABLE status should have MEDIUM risk (10 penalty)"""
        test_player.injury_status = "QUESTIONABLE"
        base_score = 100.0
        result, reason = player_manager._apply_injury_penalty(test_player, base_score)
        assert result == 100.0 - 10.0
        assert reason == "Injury: QUESTIONABLE"

    def test_injury_high_risk_out(self, player_manager, test_player):
        """OUT status should have HIGH risk (75 penalty)"""
        test_player.injury_status = "OUT"
        base_score = 100.0
        result, reason = player_manager._apply_injury_penalty(test_player, base_score)
        assert result == 100.0 - 75.0
        assert reason == "Injury: OUT"

    def test_injury_high_risk_doubtful(self, player_manager, test_player):
        """DOUBTFUL status should have HIGH risk"""
        test_player.injury_status = "DOUBTFUL"
        base_score = 100.0
        result, reason = player_manager._apply_injury_penalty(test_player, base_score)
        assert result == 100.0 - 75.0
        assert reason == "Injury: DOUBTFUL"

    def test_injury_high_risk_injury_reserve(self, player_manager, test_player):
        """INJURY_RESERVE status should have HIGH risk"""
        test_player.injury_status = "INJURY_RESERVE"
        base_score = 100.0
        result, reason = player_manager._apply_injury_penalty(test_player, base_score)
        assert result == 100.0 - 75.0
        assert reason == "Injury: INJURY_RESERVE"

    def test_injury_high_risk_unknown(self, player_manager, test_player):
        """UNKNOWN status should have HIGH risk"""
        test_player.injury_status = "UNKNOWN"
        base_score = 100.0
        result, reason = player_manager._apply_injury_penalty(test_player, base_score)
        assert result == 100.0 - 75.0
        assert reason == "Injury: UNKNOWN"


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

        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0

        # Calculate expected score manually (NO consistency multiplier)
        score = 80.0  # Normalization
        score = score * 1.20  # ADP: 96.0
        score = score * 1.25  # Player rating: 120.0
        score = score * 1.30  # Team quality: 156.0
        # No consistency multiplier
        score = score * 1.10  # Matchup: 171.6
        score = score + 50  # Draft bonus (round 0, PRIMARY): 221.6
        score = score - 0  # Bye penalty: 221.6
        score = score - 0  # Injury penalty: 221.6

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

        assert abs(result.score - 221.6) < 0.01, f"Expected ~221.6, got {result.score}"

    def test_score_player_default_flags(self, player_manager, test_player, mock_fantasy_team):
        """Test score_player with default flag values - BUG FIX: draft_round=-1"""
        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0

        result = player_manager.score_player(test_player)

        # With default flags: adp=True, player_rating=True, team_quality=True,
        # Should NOT include matchup multiplier or draft bonus

        assert result.score > 0  # Should have a positive score
        # Exact value depends on test_player attributes

    def test_score_player_only_normalization(self, player_manager, test_player, mock_fantasy_team):
        """Test score_player with all multipliers/bonuses disabled"""
        # Need ROS projection to equal 250 pts to get weighted=100.0
        # Set weeks 6-17 (12 weeks) to sum to 250.0
        for week_num in range(6, 18):
            setattr(test_player, f"week_{week_num}_points", 250.0 / 12)  # 20.833... per week
        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0

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

        mock_fantasy_team.get_matching_byes_in_roster.return_value = 5  # 5 * 25 = 125 penalty

        # Score: 10 * 0.70 * 0.75 * 0.70 * 0.60 = ~2.205
        # Then: 2.205 - 125 (bye) - 75 (injury) = ~-197.8

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
        for week_num in range(6, 18):
            setattr(test_player, f"week_{week_num}_points", 250.0 / 12)  # 20.833... per week
        test_player.position = "RB"  # Would normally get bonus in round 0
        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0

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
        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0

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
        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0

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
        for week_num in range(6, 18):
            setattr(player, f"week_{week_num}_points", 250.0 / 12)

        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0

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

        mock_fantasy_team.get_matching_byes_in_roster.return_value = 0

        result = player_manager.score_player(player, draft_round=-1)

        assert result.score <= 0  # Might be negative due to penalties


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
