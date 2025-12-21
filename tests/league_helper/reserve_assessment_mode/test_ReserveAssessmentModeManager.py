"""
Comprehensive Unit Tests for ReserveAssessmentModeManager.py

Tests the ReserveAssessmentModeManager class which identifies high-value
reserve/waiver players based on historical performance:
- Historical data loading from last_season/players.csv
- Player filtering (undrafted, HIGH risk, non-K/DST)
- 5-factor scoring algorithm
- Schedule strength calculation
- Top 15 recommendations display

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call, mock_open
from typing import List, Dict
from pathlib import Path
import csv
from io import StringIO

# Test imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from league_helper.reserve_assessment_mode.ReserveAssessmentModeManager import ReserveAssessmentModeManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
from league_helper.util.ScoredPlayer import ScoredPlayer
from utils.FantasyPlayer import FantasyPlayer


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(autouse=True)
def mock_logger():
    """Mock the logger for all tests"""
    with patch('utils.LoggingManager.get_logger') as mock_get_logger:
        mock_get_logger.return_value = Mock()
        yield mock_get_logger


@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with test config and historical data"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Create last_season subdirectory
    last_season_folder = data_folder / "last_season"
    last_season_folder.mkdir()

    # Create complete league_config.json with all required parameters
    config_content = """{
  "config_name": "Test Config",
  "description": "Test configuration for Reserve Assessment tests",
  "parameters": {
    "CURRENT_NFL_WEEK": 8,
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
      {"FLEX": "P"}
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
      "THRESHOLDS": {"VERY_POOR": 0.5, "POOR": 0.7, "GOOD": 1.1, "EXCELLENT": 1.3},
      "MULTIPLIERS": {"VERY_POOR": 0.60, "POOR": 0.80, "GOOD": 1.20, "EXCELLENT": 1.50},
      "WEIGHT": 1.0
    },
    "SCHEDULE_SCORING": {
      "IMPACT_SCALE": 80.0,
      "THRESHOLDS": {"EXCELLENT": 20, "GOOD": 16, "POOR": 12, "VERY_POOR": 8},
      "MULTIPLIERS": {"EXCELLENT": 1.25, "GOOD": 1.10, "POOR": 0.90, "VERY_POOR": 0.75},
      "WEIGHT": 1.0
    },
    "MATCHUP_SCORING": {
      "IMPACT_SCALE": 150.0,
      "THRESHOLDS": {"EXCELLENT": 15, "GOOD": 6, "POOR": -6, "VERY_POOR": -15},
      "MULTIPLIERS": {"EXCELLENT": 1.25, "GOOD": 1.10, "POOR": 0.90, "VERY_POOR": 0.75},
      "WEIGHT": 1.0
    }
  }
}"""
    config_file = data_folder / "league_config.json"
    config_file.write_text(config_content)

    return data_folder


@pytest.fixture
def config(mock_data_folder):
    """Create ConfigManager for tests"""
    return ConfigManager(mock_data_folder)


@pytest.fixture
def sample_current_players():
    """Create sample current season players (some on IR, some not)"""
    players = [
        # Undrafted HIGH risk injured players (eligible candidates)
        FantasyPlayer(
            id=1, name="Injured RB", team="KC", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0,
            average_draft_position=25.0, player_rating=85.0
        ),
        FantasyPlayer(
            id=2, name="Injured WR", team="SF", position="WR", bye_week=9,
            fantasy_points=160.0, injury_status="INJURY_RESERVE", drafted=0, locked=0,
            average_draft_position=30.0, player_rating=80.0
        ),
        FantasyPlayer(
            id=3, name="Suspended QB", team="CIN", position="QB", bye_week=10,
            fantasy_points=220.0, injury_status="SUSPENSION", drafted=0, locked=0,
            average_draft_position=15.0, player_rating=88.0
        ),

        # Undrafted but NOT injured (not eligible)
        FantasyPlayer(
            id=4, name="Healthy RB", team="BUF", position="RB", bye_week=8,
            fantasy_points=150.0, injury_status="ACTIVE", drafted=0, locked=0,
            average_draft_position=40.0, player_rating=75.0
        ),

        # Injured but DRAFTED (not eligible)
        FantasyPlayer(
            id=5, name="Drafted Injured WR", team="PHI", position="WR", bye_week=7,
            fantasy_points=190.0, injury_status="INJURY_RESERVE", drafted=1, locked=0,
            average_draft_position=20.0, player_rating=87.0
        ),

        # K and DST (excluded positions)
        FantasyPlayer(
            id=6, name="Injured K", team="BAL", position="K", bye_week=10,
            fantasy_points=100.0, injury_status="INJURY_RESERVE", drafted=0, locked=0,
            average_draft_position=100.0, player_rating=70.0
        ),
        FantasyPlayer(
            id=7, name="Injured DST", team="DAL", position="DST", bye_week=7,
            fantasy_points=95.0, injury_status="INJURY_RESERVE", drafted=0, locked=0,
            average_draft_position=80.0, player_rating=72.0
        ),
    ]
    return players


@pytest.fixture
def sample_historical_players():
    """Create sample historical (last season) players"""
    players = [
        # Historical data for "Injured RB"
        FantasyPlayer(
            id=101, name="Injured RB", team="KC", position="RB", bye_week=7,
            fantasy_points=245.0, injury_status="ACTIVE", drafted=0, locked=0,
            average_draft_position=18.0, player_rating=88.0,
            week_1_points=15.5, week_2_points=18.2, week_3_points=14.8,
            week_4_points=16.0, week_5_points=17.5, week_6_points=15.0,
            week_7_points=0.0, week_8_points=19.2, week_9_points=16.8,
            week_10_points=17.0, week_11_points=18.5, week_12_points=14.5,
            week_13_points=16.2, week_14_points=17.8, week_15_points=15.5,
            week_16_points=18.0, week_17_points=16.5
        ),

        # Historical data for "Injured WR"
        FantasyPlayer(
            id=102, name="Injured WR", team="SF", position="WR", bye_week=9,
            fantasy_points=198.0, injury_status="ACTIVE", drafted=0, locked=0,
            average_draft_position=28.0, player_rating=82.0,
            week_1_points=12.5, week_2_points=14.0, week_3_points=11.8,
            week_4_points=13.5, week_5_points=12.0, week_6_points=13.8,
            week_7_points=15.2, week_8_points=14.5, week_9_points=0.0,
            week_10_points=12.8, week_11_points=13.0, week_12_points=14.2,
            week_13_points=12.5, week_14_points=13.8, week_15_points=14.0,
            week_16_points=13.2, week_17_points=12.2
        ),

        # Historical data for "Suspended QB"
        FantasyPlayer(
            id=103, name="Suspended QB", team="CIN", position="QB", bye_week=10,
            fantasy_points=289.0, injury_status="ACTIVE", drafted=0, locked=0,
            average_draft_position=12.0, player_rating=90.0,
            week_1_points=18.5, week_2_points=22.0, week_3_points=19.8,
            week_4_points=20.5, week_5_points=21.0, week_6_points=19.5,
            week_7_points=23.2, week_8_points=20.8, week_9_points=22.5,
            week_10_points=0.0, week_11_points=21.8, week_12_points=19.2,
            week_13_points=20.0, week_14_points=22.8, week_15_points=21.5,
            week_16_points=20.2, week_17_points=19.8
        ),

        # Historical player NOT in current season (rookie this year)
        FantasyPlayer(
            id=104, name="Retired Player", team="NE", position="TE", bye_week=11,
            fantasy_points=156.0, injury_status="ACTIVE", drafted=0, locked=0,
            average_draft_position=45.0, player_rating=76.0
        ),
    ]
    return players


@pytest.fixture
def mock_player_manager(sample_current_players):
    """Create mock PlayerManager"""
    manager = Mock(spec=PlayerManager)
    manager.get_player_list.return_value = sample_current_players
    manager.players = sample_current_players  # Add players attribute for direct access
    return manager


@pytest.fixture
def mock_team_data_manager():
    """Create mock TeamDataManager"""
    manager = Mock(spec=TeamDataManager)

    # Mock team offensive/defensive ranks (for team quality multiplier)
    def get_team_offensive_rank_side_effect(team):
        team_ranks = {
            "KC": 3,
            "SF": 8,
            "CIN": 12,
            "BUF": 15,
        }
        return team_ranks.get(team, 15)

    def get_team_defensive_rank_side_effect(team):
        team_ranks = {
            "KC": 5,
            "SF": 10,
            "CIN": 20,
        }
        return team_ranks.get(team, 16)

    manager.get_team_offensive_rank.side_effect = get_team_offensive_rank_side_effect
    manager.get_team_defensive_rank.side_effect = get_team_defensive_rank_side_effect

    # Mock defense ranks (for schedule multiplier)
    def get_defense_rank_side_effect(team, position):
        defense_ranks = {
            ("BUF", "RB"): 22,
            ("NYJ", "RB"): 18,
            ("MIA", "RB"): 25,
            ("DAL", "WR"): 20,
            ("PHI", "WR"): 15,
            ("NYG", "WR"): 28,
            ("BAL", "QB"): 10,
            ("CLE", "QB"): 14,
        }
        return defense_ranks.get((team, position), 16)

    manager.get_team_defense_vs_position_rank.side_effect = get_defense_rank_side_effect

    return manager


@pytest.fixture
def mock_season_schedule_manager():
    """Create mock SeasonScheduleManager"""
    manager = Mock(spec=SeasonScheduleManager)

    # Mock future opponents
    def get_future_opponents_side_effect(team, current_week):
        schedules = {
            "KC": ["BUF", "NYJ", "MIA"],  # 3 future games
            "SF": ["DAL", "PHI", "NYG"],  # 3 future games
            "CIN": ["BAL", "CLE"],        # 2 future games
        }
        return schedules.get(team, [])

    manager.get_future_opponents.side_effect = get_future_opponents_side_effect

    return manager


@pytest.fixture
def manager(config, mock_player_manager, mock_team_data_manager,
            mock_season_schedule_manager, mock_data_folder):
    """Create ReserveAssessmentModeManager for tests"""
    # Create manager (will attempt to load historical data)
    with patch('builtins.open', mock_open(read_data="")):
        with patch('pathlib.Path.exists', return_value=False):
            manager = ReserveAssessmentModeManager(
                config=config,
                player_manager=mock_player_manager,
                team_data_manager=mock_team_data_manager,
                season_schedule_manager=mock_season_schedule_manager,
                data_folder=mock_data_folder
            )

    return manager


# ============================================================================
# HISTORICAL DATA LOADING TESTS
# ============================================================================

class TestHistoricalDataLoading:
    """Test _load_historical_data() method"""

    def test_loads_historical_data_successfully(self, config, mock_player_manager,
                                                mock_team_data_manager, mock_season_schedule_manager,
                                                mock_data_folder, sample_historical_players):
        """Test successful loading of historical player data"""
        # Create historical CSV file
        historical_csv = mock_data_folder / "last_season" / "players.csv"
        csv_data = """id,name,team,position,bye_week,fantasy_points,player_rating,injury_status,drafted,locked
101,Injured RB,KC,RB,7,245.0,88.0,ACTIVE,0,0
102,Injured WR,SF,WR,9,198.0,82.0,ACTIVE,0,0
103,Suspended QB,CIN,QB,10,289.0,90.0,ACTIVE,0,0"""
        historical_csv.write_text(csv_data)

        # Create manager (should load historical data)
        manager = ReserveAssessmentModeManager(
            config=config,
            player_manager=mock_player_manager,
            team_data_manager=mock_team_data_manager,
            season_schedule_manager=mock_season_schedule_manager,
            data_folder=mock_data_folder
        )

        # Verify historical data loaded
        assert len(manager.historical_players_dict) == 3
        assert ("injured rb", "RB") in manager.historical_players_dict
        assert ("injured wr", "WR") in manager.historical_players_dict
        assert ("suspended qb", "QB") in manager.historical_players_dict

    def test_handles_missing_historical_file(self, config, mock_player_manager,
                                             mock_team_data_manager, mock_season_schedule_manager,
                                             mock_data_folder):
        """Test graceful handling when historical file doesn't exist"""
        # Don't create historical file

        # Create manager (should handle missing file)
        manager = ReserveAssessmentModeManager(
            config=config,
            player_manager=mock_player_manager,
            team_data_manager=mock_team_data_manager,
            season_schedule_manager=mock_season_schedule_manager,
            data_folder=mock_data_folder
        )

        # Verify empty dict returned
        assert manager.historical_players_dict == {}

    def test_handles_malformed_csv_rows(self, config, mock_player_manager,
                                       mock_team_data_manager, mock_season_schedule_manager,
                                       mock_data_folder):
        """Test that malformed rows are skipped gracefully"""
        # Create CSV with one good row and one bad row
        historical_csv = mock_data_folder / "last_season" / "players.csv"
        csv_data = """id,name,team,position,bye_week,fantasy_points,player_rating,injury_status,drafted,locked
101,Injured RB,KC,RB,7,245.0,88.0,ACTIVE,0,0
999,,,INVALID,,BAD_DATA,,,"""
        historical_csv.write_text(csv_data)

        # Create manager
        manager = ReserveAssessmentModeManager(
            config=config,
            player_manager=mock_player_manager,
            team_data_manager=mock_team_data_manager,
            season_schedule_manager=mock_season_schedule_manager,
            data_folder=mock_data_folder
        )

        # Verify only valid row loaded (empty name row skipped)
        assert len(manager.historical_players_dict) == 1
        assert ("injured rb", "RB") in manager.historical_players_dict

    def test_indexes_by_name_and_position_only(self, config, mock_player_manager,
                                               mock_team_data_manager, mock_season_schedule_manager,
                                               mock_data_folder):
        """Test that indexing ignores team (to catch team changers)"""
        # Create CSV with player
        historical_csv = mock_data_folder / "last_season" / "players.csv"
        csv_data = """id,name,team,position,bye_week,fantasy_points,player_rating,injury_status,drafted,locked
101,Player Name,OLD_TEAM,RB,7,200.0,85.0,ACTIVE,0,0"""
        historical_csv.write_text(csv_data)

        # Create manager
        manager = ReserveAssessmentModeManager(
            config=config,
            player_manager=mock_player_manager,
            team_data_manager=mock_team_data_manager,
            season_schedule_manager=mock_season_schedule_manager,
            data_folder=mock_data_folder
        )

        # Verify indexed by (name.lower(), position) only
        assert ("player name", "RB") in manager.historical_players_dict
        assert manager.historical_players_dict[("player name", "RB")].team == "OLD_TEAM"


# ============================================================================
# PLAYER FILTERING TESTS
# ============================================================================

class TestPlayerFiltering:
    """Test get_recommendations() player filtering logic"""

    def test_filters_undrafted_only(self, manager, mock_player_manager, sample_current_players,
                                    sample_historical_players):
        """Test that only undrafted (drafted=0) players are considered"""
        # Setup: Add historical data so players can be scored
        manager.historical_players_dict = {
            ("injured rb", "RB"): sample_historical_players[0],
            ("injured wr", "WR"): sample_historical_players[1],
            ("suspended qb", "QB"): sample_historical_players[2],
        }

        # Call get_recommendations
        recommendations = manager.get_recommendations()

        # Verify only undrafted players included (all sample_current_players have drafted=0)
        # Note: Code accesses player_manager.players directly, not get_player_list
        assert len(recommendations) > 0  # Should have recommendations
        for scored_player in recommendations:
            assert scored_player.player.drafted == 0

    def test_filters_high_risk_only(self, manager, mock_player_manager, sample_current_players,
                                    sample_historical_players):
        """Test that only HIGH risk players are included"""
        # Add historical data
        manager.historical_players_dict = {
            ("injured rb", "RB"): sample_historical_players[0],
            ("injured wr", "WR"): sample_historical_players[1],
            ("suspended qb", "QB"): sample_historical_players[2],
            ("healthy rb", "RB"): sample_historical_players[0],  # Has historical but not injured
        }

        # Get recommendations
        recommendations = manager.get_recommendations()

        # Verify only HIGH risk players included (Injured RB, Injured WR, Suspended QB)
        # Healthy RB should be filtered out despite having historical data
        player_names = [sp.player.name for sp in recommendations]
        assert "Injured RB" in player_names
        assert "Injured WR" in player_names
        assert "Suspended QB" in player_names
        assert "Healthy RB" not in player_names

    def test_excludes_kickers_and_defense(self, manager, mock_player_manager,
                                         sample_current_players, sample_historical_players):
        """Test that K and DST positions are excluded"""
        # Add historical data for all positions
        manager.historical_players_dict = {
            ("injured rb", "RB"): sample_historical_players[0],
            ("injured k", "K"): sample_historical_players[0],  # Should be excluded
            ("injured dst", "DST"): sample_historical_players[0],  # Should be excluded
        }

        # Get recommendations
        recommendations = manager.get_recommendations()

        # Verify K and DST excluded
        player_names = [sp.player.name for sp in recommendations]
        assert "Injured RB" in player_names
        assert "Injured K" not in player_names
        assert "Injured DST" not in player_names

    def test_requires_positive_fantasy_points(self, manager, mock_player_manager):
        """Test that players with 0 or negative points are excluded"""
        # Create players with 0 and negative points
        zero_points_player = FantasyPlayer(
            id=99, name="Zero Points", team="KC", position="RB", bye_week=7,
            fantasy_points=0.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )
        negative_points_player = FantasyPlayer(
            id=98, name="Negative Points", team="SF", position="WR", bye_week=9,
            fantasy_points=-5.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )

        mock_player_manager.get_player_list.return_value = [zero_points_player, negative_points_player]
        mock_player_manager.players = [zero_points_player, negative_points_player]  # Direct access for filtering

        # Add historical data
        manager.historical_players_dict = {
            ("zero points", "RB"): zero_points_player,
            ("negative points", "WR"): negative_points_player,
        }

        # Get recommendations
        recommendations = manager.get_recommendations()

        # Verify both excluded
        assert len(recommendations) == 0

    def test_skips_players_without_historical_data(self, manager, mock_player_manager,
                                                   sample_current_players):
        """Test that players without historical data are skipped"""
        # Historical data only for some players
        manager.historical_players_dict = {
            ("injured rb", "RB"): FantasyPlayer(
                id=101, name="Injured RB", team="KC", position="RB", bye_week=7,
                fantasy_points=245.0, injury_status="ACTIVE", drafted=0, locked=0
            ),
            # "Injured WR" and "Suspended QB" have NO historical data
        }

        # Get recommendations
        recommendations = manager.get_recommendations()

        # Verify only player with historical data included
        assert len(recommendations) == 1
        assert recommendations[0].player.name == "Injured RB"


# ============================================================================
# SCORING ALGORITHM TESTS
# ============================================================================

class TestScoringAlgorithm:
    """Test _score_reserve_candidate() 5-factor scoring"""

    def test_factor1_base_score_from_historical_points(self, manager, config):
        """Test Factor 1: Base score = historical fantasy_points"""
        current_player = FantasyPlayer(
            id=1, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )
        historical_player = FantasyPlayer(
            id=101, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=245.0, injury_status="ACTIVE", drafted=0, locked=0
        )

        # Mock all manager methods to return None (no multipliers)
        # Need to clear side_effect first as it takes precedence over return_value
        manager.team_data_manager.get_team_offensive_rank.side_effect = None
        manager.team_data_manager.get_team_offensive_rank.return_value = None
        manager.team_data_manager.get_team_defensive_rank.side_effect = None
        manager.team_data_manager.get_team_defensive_rank.return_value = None
        manager.season_schedule_manager.get_future_opponents.side_effect = None
        manager.season_schedule_manager.get_future_opponents.return_value = []

        # Score player
        scored = manager._score_reserve_candidate(current_player, historical_player)

        # Verify base score equals historical points
        assert scored.score == 245.0
        assert any("Base: 245.0 pts" in reason for reason in scored.reason)

    def test_factor2_player_rating_multiplier(self, manager, config, mock_team_data_manager,
                                              mock_season_schedule_manager):
        """Test Factor 2: Player rating multiplier from historical data"""
        manager.team_data_manager = mock_team_data_manager
        manager.season_schedule_manager = mock_season_schedule_manager

        current_player = FantasyPlayer(
            id=1, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )

        # Historical player with EXCELLENT rating (>80)
        historical_player = FantasyPlayer(
            id=101, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=200.0, player_rating=85.0, injury_status="ACTIVE", drafted=0, locked=0
        )

        # Mock to avoid other multipliers (clear side_effect first)
        mock_team_data_manager.get_team_offensive_rank.side_effect = None
        mock_team_data_manager.get_team_offensive_rank.return_value = None
        mock_team_data_manager.get_team_defensive_rank.side_effect = None
        mock_team_data_manager.get_team_defensive_rank.return_value = None
        mock_season_schedule_manager.get_future_opponents.side_effect = None
        mock_season_schedule_manager.get_future_opponents.return_value = []

        # Score player
        scored = manager._score_reserve_candidate(current_player, historical_player)

        # Verify rating multiplier applied (EXCELLENT = 1.25x)
        # Base: 200.0, Rating: 1.25x = 250.0
        assert scored.score == pytest.approx(250.0, rel=0.01)
        assert any("Player Rating: EXCELLENT" in reason for reason in scored.reason)

    def test_factor3_team_quality_multiplier(self, manager, config, mock_team_data_manager,
                                            mock_season_schedule_manager):
        """Test Factor 3: Team quality multiplier from current season"""
        manager.team_data_manager = mock_team_data_manager
        manager.season_schedule_manager = mock_season_schedule_manager

        # Current player on EXCELLENT team (rank 3)
        current_player = FantasyPlayer(
            id=1, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )

        historical_player = FantasyPlayer(
            id=101, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=200.0, player_rating=None, injury_status="ACTIVE", drafted=0, locked=0
        )

        # Mock schedule (clear side_effect first)
        mock_season_schedule_manager.get_future_opponents.side_effect = None
        mock_season_schedule_manager.get_future_opponents.return_value = []

        # Score player (KC has offensive rank 3 from mock)
        scored = manager._score_reserve_candidate(current_player, historical_player)

        # Verify team quality multiplier applied (rank 3 = EXCELLENT = 1.30x)
        # Base: 200.0, Team: 1.30x = 260.0
        assert scored.score == pytest.approx(260.0, rel=0.01)
        assert any("Team Quality: EXCELLENT" in reason for reason in scored.reason)

    def test_factor4_performance_consistency_multiplier(self, manager, config,
                                                        mock_team_data_manager,
                                                        mock_season_schedule_manager):
        """Test Factor 4: Performance/consistency multiplier from weekly variance"""
        manager.team_data_manager = mock_team_data_manager
        manager.season_schedule_manager = mock_season_schedule_manager

        current_player = FantasyPlayer(
            id=1, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )

        # Historical player with consistent weekly points (low CV)
        historical_player = FantasyPlayer(
            id=101, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=200.0, player_rating=None, injury_status="ACTIVE", drafted=0, locked=0,
            week_1_points=15.0, week_2_points=16.0, week_3_points=15.5,
            week_4_points=14.5, week_5_points=15.2, week_6_points=15.8,
            week_7_points=0.0,  # Bye week
            week_8_points=15.5, week_9_points=16.2, week_10_points=14.8,
            week_11_points=15.3, week_12_points=15.7, week_13_points=15.0,
            week_14_points=15.5, week_15_points=15.9, week_16_points=14.6,
            week_17_points=15.4
        )

        # Mock to avoid other multipliers (clear side_effect first)
        mock_team_data_manager.get_team_offensive_rank.side_effect = None
        mock_team_data_manager.get_team_offensive_rank.return_value = None
        mock_team_data_manager.get_team_defensive_rank.side_effect = None
        mock_team_data_manager.get_team_defensive_rank.return_value = None
        mock_season_schedule_manager.get_future_opponents.side_effect = None
        mock_season_schedule_manager.get_future_opponents.return_value = []

        # Score player
        scored = manager._score_reserve_candidate(current_player, historical_player)

        # Verify performance multiplier present in reasons
        # (Exact value depends on CV calculation, just verify it's applied)
        assert any("Performance:" in reason for reason in scored.reason)

    def test_factor5_schedule_multiplier(self, manager, config, mock_team_data_manager,
                                        mock_season_schedule_manager):
        """Test Factor 5: Schedule strength multiplier"""
        manager.team_data_manager = mock_team_data_manager
        manager.season_schedule_manager = mock_season_schedule_manager

        # Current player on KC (has 3 future opponents from mock)
        current_player = FantasyPlayer(
            id=1, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )

        historical_player = FantasyPlayer(
            id=101, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=200.0, player_rating=None, injury_status="ACTIVE", drafted=0, locked=0
        )

        # Mock team rank
        mock_team_data_manager.get_team_offensive_rank.return_value = None
        mock_team_data_manager.get_team_defensive_rank.return_value = None

        # Score player
        scored = manager._score_reserve_candidate(current_player, historical_player)

        # Verify schedule multiplier applied
        # KC RB faces BUF(22), NYJ(18), MIA(25) = avg 21.67 (EXCELLENT)
        assert any("Schedule:" in reason for reason in scored.reason)
        assert any("EXCELLENT" in reason and "Schedule:" in reason for reason in scored.reason)

    def test_all_five_factors_combined(self, manager, config, mock_team_data_manager,
                                       mock_season_schedule_manager, sample_historical_players):
        """Test all 5 factors working together"""
        manager.team_data_manager = mock_team_data_manager
        manager.season_schedule_manager = mock_season_schedule_manager

        # Use pre-built historical player with all data
        current_player = FantasyPlayer(
            id=1, name="Injured RB", team="KC", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )
        historical_player = sample_historical_players[0]  # Has all weekly data

        # Score player
        scored = manager._score_reserve_candidate(current_player, historical_player)

        # Verify all 5 factors present
        reason_str = " ".join(scored.reason)
        assert "Base:" in reason_str
        assert "Player Rating:" in reason_str
        assert "Team Quality:" in reason_str
        assert "Performance:" in reason_str
        assert "Schedule:" in reason_str


# ============================================================================
# SCHEDULE CALCULATION TESTS
# ============================================================================

class TestScheduleCalculation:
    """Test _calculate_schedule_value() helper method"""

    def test_calculates_average_defense_rank(self, manager, mock_season_schedule_manager,
                                             mock_team_data_manager):
        """Test schedule value calculation with multiple opponents"""
        manager.season_schedule_manager = mock_season_schedule_manager
        manager.team_data_manager = mock_team_data_manager
        manager.config.current_nfl_week = 8

        player = FantasyPlayer(
            id=1, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )

        # Calculate schedule value
        schedule_value = manager._calculate_schedule_value(player)

        # Verify average of 3 opponents (BUF=22, NYJ=18, MIA=25)
        # Average = (22 + 18 + 25) / 3 = 21.67
        assert schedule_value == pytest.approx(21.67, rel=0.01)

    def test_returns_none_for_no_future_opponents(self, manager, mock_season_schedule_manager,
                                                  mock_team_data_manager):
        """Test returns None when no future games scheduled"""
        manager.season_schedule_manager = mock_season_schedule_manager
        manager.team_data_manager = mock_team_data_manager
        manager.config.current_nfl_week = 8

        # Player on team with no future opponents
        player = FantasyPlayer(
            id=1, name="Test Player", team="UNKNOWN", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )

        # Calculate schedule value
        schedule_value = manager._calculate_schedule_value(player)

        # Verify None returned
        assert schedule_value is None

    def test_returns_none_for_insufficient_future_games(self, manager, mock_season_schedule_manager,
                                                       mock_team_data_manager):
        """Test returns None when fewer than 2 future games"""
        manager.season_schedule_manager = mock_season_schedule_manager
        manager.team_data_manager = mock_team_data_manager
        manager.config.current_nfl_week = 8

        # Mock to return only 1 opponent (need to override side_effect)
        mock_season_schedule_manager.get_future_opponents.side_effect = None
        mock_season_schedule_manager.get_future_opponents.return_value = ["BUF"]

        player = FantasyPlayer(
            id=1, name="Test Player", team="KC", position="RB", bye_week=7,
            fantasy_points=180.0, injury_status="INJURY_RESERVE", drafted=0, locked=0
        )

        # Calculate schedule value
        schedule_value = manager._calculate_schedule_value(player)

        # Verify None returned (need >= 2 games)
        assert schedule_value is None


# ============================================================================
# RECOMMENDATIONS TESTS
# ============================================================================

class TestRecommendations:
    """Test get_recommendations() end-to-end"""

    def test_returns_top_15_recommendations(self, manager, mock_player_manager,
                                           sample_historical_players):
        """Test that top 15 scored players are returned"""
        # Create 20 eligible players
        eligible_players = []
        for i in range(20):
            eligible_players.append(FantasyPlayer(
                id=i, name=f"Player {i}", team="KC", position="RB", bye_week=7,
                fantasy_points=100.0 + i, injury_status="INJURY_RESERVE", drafted=0, locked=0
            ))

        mock_player_manager.get_player_list.return_value = eligible_players
        mock_player_manager.players = eligible_players  # Add for direct access

        # Add historical data for all
        manager.historical_players_dict = {
            (f"player {i}", "RB"): FantasyPlayer(
                id=100+i, name=f"Player {i}", team="KC", position="RB", bye_week=7,
                fantasy_points=200.0 + i*10, injury_status="ACTIVE", drafted=0, locked=0
            )
            for i in range(20)
        }

        # Get recommendations
        recommendations = manager.get_recommendations()

        # Verify exactly 15 returned
        assert len(recommendations) == 15

    def test_returns_fewer_than_15_if_insufficient_candidates(self, manager, mock_player_manager,
                                                              sample_current_players,
                                                              sample_historical_players):
        """Test returns all candidates if fewer than 15 eligible"""
        # Only 3 eligible players in sample_current_players
        manager.historical_players_dict = {
            ("injured rb", "RB"): sample_historical_players[0],
            ("injured wr", "WR"): sample_historical_players[1],
            ("suspended qb", "QB"): sample_historical_players[2],
        }

        # Get recommendations
        recommendations = manager.get_recommendations()

        # Verify returns 3 (all eligible)
        assert len(recommendations) == 3

    def test_recommendations_sorted_by_score_descending(self, manager, mock_player_manager,
                                                       mock_team_data_manager,
                                                       mock_season_schedule_manager):
        """Test recommendations sorted highest score first"""
        manager.team_data_manager = mock_team_data_manager
        manager.season_schedule_manager = mock_season_schedule_manager

        # Create players with different historical points
        eligible_players = [
            FantasyPlayer(id=1, name="Low Scorer", team="KC", position="RB", bye_week=7,
                         fantasy_points=100.0, injury_status="INJURY_RESERVE", drafted=0, locked=0),
            FantasyPlayer(id=2, name="High Scorer", team="KC", position="RB", bye_week=7,
                         fantasy_points=100.0, injury_status="INJURY_RESERVE", drafted=0, locked=0),
            FantasyPlayer(id=3, name="Mid Scorer", team="KC", position="RB", bye_week=7,
                         fantasy_points=100.0, injury_status="INJURY_RESERVE", drafted=0, locked=0),
        ]

        mock_player_manager.get_player_list.return_value = eligible_players
        mock_player_manager.players = eligible_players  # Direct access for filtering

        # Historical data with different scores
        manager.historical_players_dict = {
            ("low scorer", "RB"): FantasyPlayer(
                id=101, name="Low Scorer", team="KC", position="RB", bye_week=7,
                fantasy_points=150.0, injury_status="ACTIVE", drafted=0, locked=0
            ),
            ("high scorer", "RB"): FantasyPlayer(
                id=102, name="High Scorer", team="KC", position="RB", bye_week=7,
                fantasy_points=300.0, injury_status="ACTIVE", drafted=0, locked=0
            ),
            ("mid scorer", "RB"): FantasyPlayer(
                id=103, name="Mid Scorer", team="KC", position="RB", bye_week=7,
                fantasy_points=225.0, injury_status="ACTIVE", drafted=0, locked=0
            ),
        }

        # Get recommendations
        recommendations = manager.get_recommendations()

        # Verify sorted descending
        assert recommendations[0].player.name == "High Scorer"
        assert recommendations[1].player.name == "Mid Scorer"
        assert recommendations[2].player.name == "Low Scorer"

        # Verify scores are descending
        assert recommendations[0].score > recommendations[1].score
        assert recommendations[1].score > recommendations[2].score


# ============================================================================
# INTERACTIVE MODE TESTS
# ============================================================================

class TestInteractiveMode:
    """Test start_interactive_mode() display and user interaction"""

    def test_updates_manager_references(self, manager, config, mock_data_folder,
                                       mock_season_schedule_manager):
        """Test that set_managers() updates manager references"""
        # Create new manager instances
        new_player_manager = Mock(spec=PlayerManager)
        new_team_data_manager = Mock(spec=TeamDataManager)

        # Update managers
        manager.set_managers(new_player_manager, new_team_data_manager)

        # Verify references updated
        assert manager.player_manager == new_player_manager
        assert manager.team_data_manager == new_team_data_manager

    @patch('builtins.input', return_value='')  # Mock Enter keypress
    @patch('builtins.print')
    def test_displays_recommendations(self, mock_print, mock_input, manager,
                                     mock_player_manager, mock_team_data_manager,
                                     sample_current_players,
                                     sample_historical_players):
        """Test display of recommendations to user"""
        # Add historical data
        manager.historical_players_dict = {
            ("injured rb", "RB"): sample_historical_players[0],
            ("injured wr", "WR"): sample_historical_players[1],
        }

        # Run interactive mode
        manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

        # Verify header printed
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("RESERVE ASSESSMENT" in str(call) for call in calls)
        assert any("High-Value Injured Players" in str(call) for call in calls)

    @patch('builtins.input', return_value='')
    @patch('builtins.print')
    def test_displays_no_candidates_message(self, mock_print, mock_input, manager,
                                           mock_player_manager):
        """Test message when no candidates found"""
        # No historical data (no matches)
        manager.historical_players_dict = {}

        # Run interactive mode
        manager.start_interactive_mode(mock_player_manager, Mock(spec=TeamDataManager))

        # Verify "no candidates" message
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("No reserve candidates found" in str(call) for call in calls)

    @patch('builtins.input', return_value='')
    def test_waits_for_user_input(self, mock_input, manager, mock_player_manager):
        """Test that mode waits for Enter before returning"""
        # Run interactive mode
        manager.start_interactive_mode(mock_player_manager, Mock(spec=TeamDataManager))

        # Verify input() was called
        mock_input.assert_called_once()
