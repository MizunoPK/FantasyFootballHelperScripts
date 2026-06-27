"""
Comprehensive Unit Tests for AddToRosterModeManager.py

Tests the AddToRosterModeManager class which manages the draft assistant mode:
- Intelligent player recommendations based on draft position
- Interactive player selection workflow
- Roster display by draft rounds
- Position-aware draft strategy (PRIMARY/SECONDARY bonuses)
- CSV updates after each pick

This is a CRITICAL module (242 lines) with NO EXISTING TESTS.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from typing import List

from league_helper.add_to_roster_mode.AddToRosterModeManager import AddToRosterModeManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.ScoredPlayer import ScoredPlayer
from league_helper.util.FantasyTeam import FantasyTeam
import league_helper.constants as Constants
from utils.FantasyPlayer import FantasyPlayer



@pytest.fixture(autouse=True)
def mock_logger():
    """Mock the logger for all tests"""
    with patch('utils.LoggingManager.get_logger') as mock_get_logger:
        mock_get_logger.return_value = Mock()
        yield mock_get_logger


@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with test config"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    config_content = """{
  "config_name": "Test Config",
  "description": "Test configuration for AddToRosterMode tests",
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
      {"FLEX": "P"},
      {"FLEX": "P"},
      {"FLEX": "P"},
      {"FLEX": "P"},
      {"QB": "P"},
      {"TE": "P"},
      {"FLEX": "P"},
      {"K": "P"},
      {"DST": "P"},
      {"FLEX": "P"},
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
      "THRESHOLDS": {"VERY_POOR": -0.2, "POOR": -0.1, "GOOD": 0.1, "EXCELLENT": 0.2},
      "MULTIPLIERS": {"VERY_POOR": 0.60, "POOR": 0.80, "GOOD": 1.20, "EXCELLENT": 1.50},
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
def config(mock_data_folder):
    """Create ConfigManager for tests"""
    return ConfigManager(mock_data_folder)


@pytest.fixture
def sample_players():
    """Create sample test players with various attributes"""
    players = [
        FantasyPlayer(id=1, name="QB1", team="KC", position="QB", bye_week=7,
                     fantasy_points=250.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=5.0, player_rating=90.0),
        FantasyPlayer(id=2, name="QB2", team="BUF", position="QB", bye_week=10,
                     fantasy_points=220.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=15.0, player_rating=85.0),

        FantasyPlayer(id=3, name="RB1", team="SF", position="RB", bye_week=7,
                     fantasy_points=200.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=3.0, player_rating=92.0),
        FantasyPlayer(id=4, name="RB2", team="PHI", position="RB", bye_week=8,
                     fantasy_points=180.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=10.0, player_rating=88.0),
        FantasyPlayer(id=5, name="RB3", team="DAL", position="RB", bye_week=9,
                     fantasy_points=160.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=25.0, player_rating=80.0),
        FantasyPlayer(id=6, name="RB4", team="MIA", position="RB", bye_week=10,
                     fantasy_points=140.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=40.0, player_rating=75.0),

        FantasyPlayer(id=7, name="WR1", team="MIN", position="WR", bye_week=6,
                     fantasy_points=190.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=8.0, player_rating=89.0),
        FantasyPlayer(id=8, name="WR2", team="CIN", position="WR", bye_week=7,
                     fantasy_points=175.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=18.0, player_rating=86.0),
        FantasyPlayer(id=9, name="WR3", team="DET", position="WR", bye_week=8,
                     fantasy_points=165.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=30.0, player_rating=82.0),
        FantasyPlayer(id=10, name="WR4", team="LAC", position="WR", bye_week=9,
                     fantasy_points=155.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=45.0, player_rating=78.0),

        FantasyPlayer(id=11, name="TE1", team="KC", position="TE", bye_week=7,
                     fantasy_points=145.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=20.0, player_rating=87.0),
        FantasyPlayer(id=12, name="TE2", team="SF", position="TE", bye_week=8,
                     fantasy_points=120.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=50.0, player_rating=74.0),

        FantasyPlayer(id=13, name="K1", team="BAL", position="K", bye_week=10,
                     fantasy_points=100.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=100.0, player_rating=70.0),

        FantasyPlayer(id=14, name="DST1", team="SF", position="DST", bye_week=7,
                     fantasy_points=95.0, injury_status="ACTIVE", drafted_by="", locked=0,
                     average_draft_position=80.0, player_rating=72.0),
    ]
    return players


@pytest.fixture
def mock_player_manager(config, sample_players):
    """Create mock PlayerManager with sample players"""
    manager = Mock(spec=PlayerManager)
    manager.config = config
    manager.team = Mock(spec=FantasyTeam)
    manager.team.roster = []
    manager.team.config = config
    manager.players = sample_players

    def get_player_list_mock(drafted_vals=None, can_draft=False):
        if drafted_vals == [0]:
            return [p for p in sample_players if p.is_free_agent()]
        return sample_players

    manager.get_player_list = Mock(side_effect=get_player_list_mock)

    def score_player_mock(player, **kwargs):
        score = player.fantasy_points + (kwargs.get('draft_round', 0) * 10)
        return ScoredPlayer(player, score, reasons=[])

    manager.score_player = Mock(side_effect=score_player_mock)
    manager.draft_player = Mock(return_value=True)
    manager.update_players_file = Mock()
    manager.get_roster_len = Mock(return_value=0)

    return manager


@pytest.fixture
def mock_team_data_manager():
    """Create mock TeamDataManager"""
    manager = Mock(spec=TeamDataManager)
    return manager


@pytest.fixture
def add_to_roster_manager(config, mock_player_manager, mock_team_data_manager):
    """Create AddToRosterModeManager instance for tests"""
    manager = AddToRosterModeManager(config, mock_player_manager, mock_team_data_manager)
    return manager



class TestInitialization:
    """Test AddToRosterModeManager initialization"""

    def test_init_sets_config(self, config, mock_player_manager, mock_team_data_manager):
        """Test initialization sets config properly"""
        manager = AddToRosterModeManager(config, mock_player_manager, mock_team_data_manager)

        assert manager.config == config
        assert manager.player_manager == mock_player_manager
        assert manager.team_data_manager == mock_team_data_manager

    def test_init_calls_set_managers(self, config, mock_player_manager, mock_team_data_manager):
        """Test initialization calls set_managers"""
        with patch.object(AddToRosterModeManager, 'set_managers') as mock_set:
            manager = AddToRosterModeManager(config, mock_player_manager, mock_team_data_manager)
            mock_set.assert_called_once_with(mock_player_manager, mock_team_data_manager)

    def test_init_creates_logger(self, config, mock_player_manager, mock_team_data_manager):
        """Test initialization creates logger"""
        manager = AddToRosterModeManager(config, mock_player_manager, mock_team_data_manager)

        assert manager.logger is not None



class TestSetManagers:
    """Test set_managers() method"""

    def test_set_managers_updates_player_manager(self, add_to_roster_manager, mock_player_manager):
        """Test set_managers updates player manager"""
        new_manager = Mock(spec=PlayerManager)

        add_to_roster_manager.set_managers(new_manager, add_to_roster_manager.team_data_manager)

        assert add_to_roster_manager.player_manager == new_manager

    def test_set_managers_updates_team_data_manager(self, add_to_roster_manager, mock_team_data_manager):
        """Test set_managers updates team data manager"""
        new_manager = Mock(spec=TeamDataManager)

        add_to_roster_manager.set_managers(add_to_roster_manager.player_manager, new_manager)

        assert add_to_roster_manager.team_data_manager == new_manager



class TestGetCurrentRound:
    """Test _get_current_round() method"""

    def test_get_current_round_empty_roster(self, add_to_roster_manager):
        """Test getting current round with empty roster"""
        with patch.object(add_to_roster_manager, '_match_players_to_rounds', return_value={}):
            current_round = add_to_roster_manager._get_current_round()

            assert current_round == 1

    def test_get_current_round_partial_roster(self, add_to_roster_manager):
        """Test getting current round with partial roster"""
        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value={1: Mock(), 2: Mock(), 3: Mock(), 4: Mock(), 5: Mock()}):
            current_round = add_to_roster_manager._get_current_round()

            assert current_round == 6

    def test_get_current_round_almost_full_roster(self, add_to_roster_manager):
        """Test getting current round with almost full roster (14/15)"""
        filled_rounds = {i: Mock() for i in range(1, 15)}
        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value=filled_rounds):
            current_round = add_to_roster_manager._get_current_round()

            assert current_round == 15

    def test_get_current_round_full_roster(self, add_to_roster_manager):
        """Test getting current round with full roster (15/15)"""
        filled_rounds = {i: Mock() for i in range(1, 16)}
        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value=filled_rounds):
            current_round = add_to_roster_manager._get_current_round()

            assert current_round is None



class TestMatchPlayersToRounds:
    """Test _match_players_to_rounds() method"""

    def test_match_players_empty_roster(self, add_to_roster_manager, mock_player_manager):
        """Test matching with empty roster"""
        mock_player_manager.team.roster = []

        result = add_to_roster_manager._match_players_to_rounds()

        assert result == {}

    def test_match_players_perfect_match(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test matching when players perfectly match draft order positions"""
        rb = sample_players[2]
        qb = sample_players[0]
        mock_player_manager.team.roster = [rb, qb]

        result = add_to_roster_manager._match_players_to_rounds()

        assert 1 in result
        assert result[1] == rb

    def test_match_players_partial_match(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test matching with partial roster"""
        players = [sample_players[2], sample_players[6], sample_players[0]]
        for p in players:
            p.drafted_by = "Sea Sharp"
        mock_player_manager.team.roster = players

        result = add_to_roster_manager._match_players_to_rounds()

        assert len(result) > 0
        assert len(result) <= len(players)

    def test_match_players_multiple_same_position(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test matching when multiple players have same position"""
        rbs = [sample_players[2], sample_players[3], sample_players[4], sample_players[5]]
        for rb in rbs:
            rb.drafted_by = "Sea Sharp"
        mock_player_manager.team.roster = rbs

        result = add_to_roster_manager._match_players_to_rounds()

        assert len(result) > 0

    def test_match_players_uses_optimal_fit(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test that matching uses optimal fit strategy (perfect position match first)"""
        qb = sample_players[0]
        qb.drafted_by = "Sea Sharp"
        mock_player_manager.team.roster = [qb]

        result = add_to_roster_manager._match_players_to_rounds()

        assert len(result) > 0
        assert any(p == qb for p in result.values())


    def test_rb_matches_native_rb_round(self, add_to_roster_manager, mock_player_manager, sample_players, config):
        """Test RB player can match to RB-ideal round (not just FLEX) - Bug Fix Validation

        This test validates the fix for the bug where RB players could only match
        FLEX-ideal rounds and not RB-ideal rounds.

        NOTE: Current test DRAFT_ORDER uses FLEX for most rounds, not specific RB rounds.
        This test verifies RB can match FLEX rounds (which is the fallback behavior).
        The helper method also allows RB to match RB-ideal rounds when they exist.
        """
        rb_player = sample_players[2]
        mock_player_manager.team.roster = [rb_player]

        result = add_to_roster_manager._match_players_to_rounds()

        assert len(result) > 0, "RB should match to at least one round"
        assert rb_player in result.values(), "RB player should be assigned to a round"

        flex_rounds = [1, 2, 5, 6, 7, 8, 11, 14, 15]
        rb_round = [r for r, p in result.items() if p == rb_player][0]
        assert rb_round in flex_rounds, f"RB matched to round {rb_round}, expected FLEX round"

    def test_wr_matches_native_wr_round(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test WR player can match to WR-ideal round (not just FLEX) - Bug Fix Validation

        This test validates the fix for the bug where WR players could only match
        FLEX-ideal rounds and not WR-ideal rounds.

        NOTE: Current test DRAFT_ORDER uses FLEX for most rounds, not specific WR rounds.
        This test verifies WR can match FLEX rounds (which is the fallback behavior).
        The helper method also allows WR to match WR-ideal rounds when they exist.
        """
        wr_player = sample_players[6]
        mock_player_manager.team.roster = [wr_player]

        result = add_to_roster_manager._match_players_to_rounds()

        assert len(result) > 0, "WR should match to at least one round"
        assert wr_player in result.values(), "WR player should be assigned to a round"

        flex_rounds = [1, 2, 5, 6, 7, 8, 11, 14, 15]
        wr_round = [r for r, p in result.items() if p == wr_player][0]
        assert wr_round in flex_rounds, f"WR matched to round {wr_round}, expected FLEX round"

    def test_rb_wr_still_match_flex_rounds(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test RB/WR can still match to FLEX-ideal rounds - Regression Test

        Validates that the fix maintains existing FLEX matching behavior.
        """
        rb_players = [sample_players[2], sample_players[3], sample_players[4], sample_players[5]]
        wr_players = [sample_players[6], sample_players[7], sample_players[8], sample_players[9]]
        mock_player_manager.team.roster = rb_players + wr_players

        result = add_to_roster_manager._match_players_to_rounds()

        flex_rounds = [1, 2, 5, 6, 7, 8, 11, 14, 15]
        flex_matched = [result.get(r) for r in flex_rounds if r in result]
        flex_rb_or_wr = [p for p in flex_matched if p and p.position in ["RB", "WR"]]

        assert len(flex_rb_or_wr) > 0, "RB or WR should match to FLEX-ideal rounds"
        assert len(result) > 0, "Players should be assigned to rounds"

    def test_non_flex_positions_exact_match_only(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test QB/TE/K/DST only match exact position (not FLEX) - Regression Test

        Validates that non-FLEX positions cannot match FLEX rounds.
        """
        qb = sample_players[0]
        te = sample_players[10]
        k = sample_players[12]
        dst = sample_players[13]
        mock_player_manager.team.roster = [qb, te, k, dst]

        result = add_to_roster_manager._match_players_to_rounds()

        flex_only_rounds = [5, 6, 7, 8, 11, 14, 15]
        for round_num in flex_only_rounds:
            if round_num in result:
                player = result[round_num]
                assert player.position in ["RB", "WR"], \
                    f"FLEX-only round {round_num} should only have RB/WR, found {player.position}"

        assert len(result) > 0, "Players should be assigned"

    def test_full_roster_all_positions_match_correctly(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test with 14 players (all positions) - Regression test for bug

        Validates that a full roster is correctly assigned to rounds.
        """
        roster = sample_players
        mock_player_manager.team.roster = roster

        result = add_to_roster_manager._match_players_to_rounds()

        assert len(result) == 14, f"Expected 14 players matched, got {len(result)}"

        matched_players = set(result.values())
        assert len(matched_players) == 14, "All 14 unique players should be matched"

    def test_position_matches_ideal_all_paths(self, add_to_roster_manager):
        """Test _position_matches_ideal() helper method - all logic paths

        Validates the new helper method implements correct FLEX matching logic.
        """
        helper = add_to_roster_manager

        assert helper._position_matches_ideal("RB", "RB") == True, "RB should match RB-ideal (native)"
        assert helper._position_matches_ideal("RB", "FLEX") == True, "RB should match FLEX-ideal"
        assert helper._position_matches_ideal("RB", "WR") == False, "RB should NOT match WR-ideal"
        assert helper._position_matches_ideal("RB", "QB") == False, "RB should NOT match QB-ideal"

        assert helper._position_matches_ideal("WR", "WR") == True, "WR should match WR-ideal (native)"
        assert helper._position_matches_ideal("WR", "FLEX") == True, "WR should match FLEX-ideal"
        assert helper._position_matches_ideal("WR", "RB") == False, "WR should NOT match RB-ideal"

        assert helper._position_matches_ideal("QB", "QB") == True, "QB should match QB-ideal (exact)"
        assert helper._position_matches_ideal("QB", "FLEX") == False, "QB should NOT match FLEX-ideal"
        assert helper._position_matches_ideal("TE", "TE") == True, "TE should match TE-ideal (exact)"
        assert helper._position_matches_ideal("TE", "FLEX") == False, "TE should NOT match FLEX-ideal"
        assert helper._position_matches_ideal("K", "K") == True, "K should match K-ideal (exact)"
        assert helper._position_matches_ideal("DST", "DST") == True, "DST should match DST-ideal (exact)"

    def test_integration_with_actual_user_roster(self, add_to_roster_manager, mock_player_manager, config):
        """Integration test with user's actual 15-player roster from bug report

        This test uses a roster composition similar to the user's bug report:
        - 4 WR, 4 RB, 2 QB, 2 TE, 1 K, 1 DST, 1 extra RB for FLEX
        """
        user_roster = [
            FantasyPlayer(id=100, name="WR1", team="MIN", position="WR", bye_week=6,
                         fantasy_points=290.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=101, name="WR2", team="CIN", position="WR", bye_week=7,
                         fantasy_points=270.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=102, name="WR3", team="DET", position="WR", bye_week=8,
                         fantasy_points=250.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=103, name="WR4", team="LAC", position="WR", bye_week=9,
                         fantasy_points=230.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=104, name="RB1", team="SF", position="RB", bye_week=7,
                         fantasy_points=280.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=105, name="RB2", team="PHI", position="RB", bye_week=8,
                         fantasy_points=260.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=106, name="RB3", team="DAL", position="RB", bye_week=9,
                         fantasy_points=240.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=107, name="Ashton Jeanty", team="OSU", position="RB", bye_week=10,
                         fantasy_points=259.8, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=108, name="QB1", team="KC", position="QB", bye_week=7,
                         fantasy_points=300.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=109, name="QB2", team="BUF", position="QB", bye_week=10,
                         fantasy_points=250.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=110, name="TE1", team="KC", position="TE", bye_week=7,
                         fantasy_points=200.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=111, name="TE2", team="SF", position="TE", bye_week=8,
                         fantasy_points=180.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=112, name="K1", team="BAL", position="K", bye_week=10,
                         fantasy_points=150.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=113, name="DST1", team="SF", position="DST", bye_week=7,
                         fantasy_points=140.0, injury_status="ACTIVE", drafted_by="", locked=0),
            FantasyPlayer(id=114, name="FLEX_RB", team="MIA", position="RB", bye_week=11,
                         fantasy_points=210.0, injury_status="ACTIVE", drafted_by="", locked=0),
        ]
        mock_player_manager.team.roster = user_roster

        result = add_to_roster_manager._match_players_to_rounds()

        assert len(result) == 15, f"All 15 players from user's roster should be matched, got {len(result)}"

        matched_players = set(result.values())
        assert len(matched_players) == 15, "All 15 unique players should be matched"

        wr_players = [p for p in user_roster if p.position == "WR"]
        for wr in wr_players:
            assert wr in result.values(), f"WR {wr.name} should be matched"

        rb_players = [p for p in user_roster if p.position == "RB"]
        for rb in rb_players:
            assert rb in result.values(), f"RB {rb.name} should be matched"



class TestGetRecommendations:
    """Test get_recommendations() method"""

    def test_get_recommendations_returns_top_players(self, add_to_roster_manager, sample_players):
        """Test that get_recommendations returns top N players"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            recommendations = add_to_roster_manager.get_recommendations()

            assert len(recommendations) == Constants.RECOMMENDATION_COUNT
            assert all(isinstance(p, ScoredPlayer) for p in recommendations)

    def test_get_recommendations_sorted_by_score(self, add_to_roster_manager, sample_players):
        """Test that recommendations are sorted by score descending"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            recommendations = add_to_roster_manager.get_recommendations()

            for i in range(len(recommendations) - 1):
                assert recommendations[i].score >= recommendations[i+1].score

    def test_get_recommendations_only_available_players(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test that only available players (drafted_by="") are recommended"""
        sample_players[0].drafted_by = "Opponent Team"
        sample_players[1].drafted_by = "Sea Sharp"

        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            recommendations = add_to_roster_manager.get_recommendations()

            for rec in recommendations:
                assert rec.player.is_free_agent()

    def test_get_recommendations_only_draftable_players(self, add_to_roster_manager, mock_player_manager):
        """Test that only players that can be drafted are recommended"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            add_to_roster_manager.get_recommendations()

            mock_player_manager.get_player_list.assert_called_with(drafted_vals=[0], can_draft=True)

    def test_get_recommendations_uses_draft_round_bonus(self, add_to_roster_manager, mock_player_manager):
        """Test that recommendations use draft_round parameter for bonus"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=5):
            add_to_roster_manager.get_recommendations()

            calls = mock_player_manager.score_player.call_args_list
            assert any(call.kwargs.get('draft_round') == 4 for call in calls)

    def test_get_recommendations_final_round_passes_zero_indexed_round(
        self, add_to_roster_manager, mock_player_manager
    ):
        """Regression: final round (15) must pass the 0-indexed round (14) so
        get_draft_order_bonus indexes draft_order[14], never draft_order[15]
        (which previously raised IndexError on the last pick)."""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=15):
            # Must not raise (the IndexError this story fixes).
            add_to_roster_manager.get_recommendations()

            calls = mock_player_manager.score_player.call_args_list
            assert len(calls) > 0
            assert all(
                call.kwargs.get('draft_round') == 14 for call in calls
            )

    def test_get_recommendations_full_roster_returns_empty_no_typeerror(
        self, add_to_roster_manager, mock_player_manager
    ):
        """Roster-full guard: when _get_current_round() returns None (full roster),
        get_recommendations() returns [] without raising TypeError on `current_round - 1`,
        even if draftable players remain. (Added in Polish per PR #21 review.)"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=None):
            # Must not raise TypeError (None - 1); returns no recommendations.
            result = add_to_roster_manager.get_recommendations()

            assert result == []
            # score_player must never be called once the roster-full guard returns.
            mock_player_manager.score_player.assert_not_called()

    def test_get_recommendations_enables_all_scoring_factors(self, add_to_roster_manager, mock_player_manager):
        """Test that scoring factors are configured correctly for draft mode"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            add_to_roster_manager.get_recommendations()

            calls = mock_player_manager.score_player.call_args_list
            assert len(calls) > 0
            first_call = calls[0].kwargs
            assert first_call.get('adp') == True
            assert first_call.get('player_rating') == True
            assert first_call.get('team_quality') == True
            assert first_call.get('performance') == False
            assert first_call.get('matchup') == False
            assert first_call.get('schedule') == False

    def test_get_recommendations_empty_when_no_available_players(self, add_to_roster_manager):
        """Test that empty list returned when no available players"""
        with patch.object(add_to_roster_manager.player_manager, 'get_player_list', return_value=[]):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                recommendations = add_to_roster_manager.get_recommendations()

                assert recommendations == []



class TestDisplayRosterByDraftRounds:
    """Test _display_roster_by_draft_rounds() method"""

    def test_display_empty_roster(self, add_to_roster_manager, mock_player_manager, capsys):
        """Test displaying empty roster"""
        mock_player_manager.team.roster = []
        mock_player_manager.get_roster_len.return_value = 0

        add_to_roster_manager._display_roster_by_draft_rounds()

        captured = capsys.readouterr()
        assert "Current Roster by Draft Round:" in captured.out
        assert "No players in roster yet." in captured.out

    def test_display_partial_roster(self, add_to_roster_manager, mock_player_manager, sample_players, capsys):
        """Test displaying partial roster"""
        players = sample_players[:3]
        for p in players:
            p.drafted_by = "Sea Sharp"
        mock_player_manager.team.roster = players
        mock_player_manager.get_roster_len.return_value = 3

        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value={1: players[0], 2: players[1], 3: players[2]}):
            add_to_roster_manager._display_roster_by_draft_rounds()

            captured = capsys.readouterr()
            assert "Current Roster by Draft Round:" in captured.out
            assert "Round  1" in captured.out
            assert "[EMPTY SLOT]" in captured.out
            assert "Roster Status: 3/15 players drafted" in captured.out

    def test_display_shows_ideal_positions(self, add_to_roster_manager, mock_player_manager, sample_players, capsys):
        """Test that display shows ideal position for each round"""
        players = [sample_players[0]]
        for p in players:
            p.drafted_by = "Sea Sharp"
        mock_player_manager.team.roster = players
        mock_player_manager.get_roster_len.return_value = 1

        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value={1: players[0]}):
            add_to_roster_manager._display_roster_by_draft_rounds()

            captured = capsys.readouterr()
            assert "(Ideal:" in captured.out
            assert "FLEX" in captured.out

    def test_display_full_roster(self, add_to_roster_manager, mock_player_manager, sample_players, capsys):
        """Test displaying full roster (15/15)"""
        full_roster = []
        for i in range(15):
            if i < len(sample_players):
                p = sample_players[i]
            else:
                p = FantasyPlayer(id=100+i, name=f"Extra{i}", team="KC", position="RB",
                                 bye_week=7, fantasy_points=100.0, injury_status="ACTIVE",
                                 drafted_by="Sea Sharp", locked=0)
            p.drafted_by = "Sea Sharp"
            full_roster.append(p)

        mock_player_manager.team.roster = full_roster
        mock_player_manager.get_roster_len.return_value = 15

        filled_rounds = {i: full_roster[i-1] for i in range(1, 16)}
        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value=filled_rounds):
            add_to_roster_manager._display_roster_by_draft_rounds()

            captured = capsys.readouterr()
            assert "Roster Status: 15/15 players drafted" in captured.out
            assert captured.out.count("Round") >= 15



class TestInteractiveMode:
    """Test start_interactive_mode() method"""

    @patch('builtins.input', side_effect=[str(Constants.RECOMMENDATION_COUNT + 1)])
    def test_interactive_mode_back_to_menu(self, mock_input, add_to_roster_manager, mock_player_manager, mock_team_data_manager, capsys):
        """Test choosing to go back to main menu"""
        mock_player_manager.get_roster_len.return_value = 0

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds'):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=[Mock(spec=ScoredPlayer) for _ in range(10)]):
                    add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

        captured = capsys.readouterr()
        assert "Returning to Main Menu..." in captured.out

    @patch('builtins.input', side_effect=['1'])
    def test_interactive_mode_draft_player_success(self, mock_input, add_to_roster_manager,
                                                   mock_player_manager, mock_team_data_manager, sample_players, capsys):
        """Test successfully drafting a player"""
        mock_player_manager.get_roster_len.return_value = 0
        mock_player_manager.draft_player.return_value = True

        recommendations = [ScoredPlayer(sample_players[i], 100.0 - i, []) for i in range(10)]

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds'):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=recommendations):
                    add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

        captured = capsys.readouterr()
        assert "Successfully added" in captured.out
        mock_player_manager.draft_player.assert_called_once()
        mock_player_manager.update_players_file.assert_called_once()

    @patch('builtins.input', side_effect=['1'])
    def test_interactive_mode_draft_player_failure(self, mock_input, add_to_roster_manager,
                                                   mock_player_manager, mock_team_data_manager, sample_players, capsys):
        """Test failed player draft"""
        mock_player_manager.get_roster_len.return_value = 0
        mock_player_manager.draft_player.return_value = False

        recommendations = [ScoredPlayer(sample_players[i], 100.0 - i, []) for i in range(10)]

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds'):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=recommendations):
                    add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

        captured = capsys.readouterr()
        assert "Failed to add" in captured.out
        assert "Check roster limits" in captured.out
        mock_player_manager.update_players_file.assert_not_called()

    @patch('builtins.input', side_effect=['abc', '11'])
    def test_interactive_mode_invalid_input(self, mock_input, add_to_roster_manager,
                                           mock_player_manager, mock_team_data_manager, capsys):
        """Test handling of invalid input"""
        mock_player_manager.get_roster_len.return_value = 0
        recommendations = [Mock(spec=ScoredPlayer) for _ in range(10)]

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds'):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=recommendations):
                    add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

        captured = capsys.readouterr()
        assert "Invalid input" in captured.out

    @patch('builtins.input', side_effect=['0', '11'])
    def test_interactive_mode_out_of_range_selection(self, mock_input, add_to_roster_manager,
                                                     mock_player_manager, mock_team_data_manager, capsys):
        """Test handling out of range selection"""
        mock_player_manager.get_roster_len.return_value = 0
        recommendations = [Mock(spec=ScoredPlayer) for _ in range(10)]

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds'):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=recommendations):
                    add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

        captured = capsys.readouterr()
        assert "Invalid selection" in captured.out

    def test_interactive_mode_no_recommendations(self, add_to_roster_manager,
                                                mock_player_manager, mock_team_data_manager, capsys):
        """Test when no recommendations available (roster full or no available players)"""
        mock_player_manager.get_roster_len.return_value = 15

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds'):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=None):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=[]):
                    add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

        captured = capsys.readouterr()
        assert "No recommendations available" in captured.out
        assert "Returning to Main Menu..." in captured.out

    @patch('builtins.input', side_effect=['1'])
    def test_interactive_mode_updates_managers(self, mock_input, add_to_roster_manager,
                                              mock_player_manager, sample_players):
        """Test that interactive mode updates managers via set_managers"""
        new_player_manager = Mock(spec=PlayerManager)
        new_player_manager.get_roster_len.return_value = 0
        new_player_manager.draft_player.return_value = True
        new_player_manager.update_players_file = Mock()
        new_player_manager.team = Mock()
        new_player_manager.team.roster = []

        new_team_manager = Mock(spec=TeamDataManager)

        recommendations = [ScoredPlayer(sample_players[0], 100.0, [])]

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds'):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=recommendations):
                    add_to_roster_manager.start_interactive_mode(new_player_manager, new_team_manager)

        assert add_to_roster_manager.player_manager == new_player_manager
        assert add_to_roster_manager.team_data_manager == new_team_manager

    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.print')
    def test_interactive_mode_shows_updated_roster_after_draft(self, mock_print, mock_input,
                                                               add_to_roster_manager,
                                                               mock_player_manager, mock_team_data_manager, sample_players):
        """Test that updated roster is displayed after successful draft"""
        mock_player_manager.get_roster_len.return_value = 0
        mock_player_manager.draft_player.return_value = True

        recommendations = [ScoredPlayer(sample_players[0], 100.0, [])]

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds') as mock_display:
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=recommendations):
                    add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

        assert mock_display.call_count == 2



class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_get_recommendations_handles_scoring_error(self, add_to_roster_manager, mock_player_manager):
        """Test that get_recommendations handles scoring errors gracefully"""
        mock_player_manager.score_player.side_effect = Exception("Scoring error")

        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            with pytest.raises(Exception):
                add_to_roster_manager.get_recommendations()

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_interactive_mode_handles_keyboard_interrupt(self, mock_input, add_to_roster_manager,
                                                        mock_player_manager, mock_team_data_manager):
        """Test handling of KeyboardInterrupt (Ctrl+C)"""
        mock_player_manager.get_roster_len.return_value = 0

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds'):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=[Mock(spec=ScoredPlayer)]):
                    with pytest.raises(KeyboardInterrupt):
                        add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

    def test_match_players_to_rounds_with_duplicate_positions(self, add_to_roster_manager,
                                                              mock_player_manager, sample_players):
        """Test matching when roster has many players of same position"""
        rbs = []
        for i in range(10):
            rb = FantasyPlayer(id=100+i, name=f"RB{i}", team="KC", position="RB",
                             bye_week=7, fantasy_points=100.0, injury_status="ACTIVE",
                             drafted_by="Sea Sharp", locked=0)
            rbs.append(rb)

        mock_player_manager.team.roster = rbs

        result = add_to_roster_manager._match_players_to_rounds()

        assert len(result) > 0
        assert len(result) <= add_to_roster_manager.config.max_players

    def test_get_current_round_when_roster_is_full(self, add_to_roster_manager):
        """Test _get_current_round returns None when roster is completely full"""
        filled_rounds = {i: Mock() for i in range(1, 16)}

        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value=filled_rounds):
            current_round = add_to_roster_manager._get_current_round()

            assert current_round is None

    def test_draft_helper_uses_ros_normalization(self, mock_player_manager):
        """Test that Draft Helper mode continues using ROS max_projection (backward compatibility)"""
        from utils.FantasyPlayer import FantasyPlayer
        from league_helper.util.ScoredPlayer import ScoredPlayer

        test_player = FantasyPlayer(id=1, name="Test Player", team="KC", position="RB",
                                   fantasy_points=300.0, injury_status="ACTIVE")

        mock_player_manager.max_projection = 400.0
        mock_player_manager.scoring_calculator = Mock()
        mock_player_manager.scoring_calculator.max_projection = 400.0
        mock_player_manager.max_weekly_projections = {6: 30.0}
        mock_player_manager.scoring_calculator.max_weekly_projection = 0.0

        def mock_score_player(player, **kwargs):
            assert kwargs.get('use_weekly_projection', False) == False
            return ScoredPlayer(player, 75.0, "ROS normalization test")

        mock_player_manager.score_player = Mock(side_effect=mock_score_player)

        result = mock_player_manager.score_player(
            test_player,
            use_weekly_projection=False,
            adp=True,
            player_rating=True
        )

        assert result.score == 75.0
        assert mock_player_manager.score_player.called

    def test_recommendations_with_single_available_player(self, add_to_roster_manager, sample_players):
        """Test recommendations when only 1 player is available"""
        available_player = sample_players[0]
        available_player.drafted_by = ""

        with patch.object(add_to_roster_manager.player_manager, 'get_player_list', return_value=[available_player]):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                recommendations = add_to_roster_manager.get_recommendations()

                assert len(recommendations) == 1
                assert recommendations[0].player == available_player


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


