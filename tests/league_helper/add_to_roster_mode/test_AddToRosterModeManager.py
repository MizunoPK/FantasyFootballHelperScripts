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
from pathlib import Path

# Test imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from league_helper.add_to_roster_mode.AddToRosterModeManager import AddToRosterModeManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.ScoredPlayer import ScoredPlayer
from league_helper.util.FantasyTeam import FantasyTeam
import league_helper.constants as Constants
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
    """Create temporary data folder with test config"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Create complete league_config.json with all required parameters
    config_content = """{
  "config_name": "Test Config",
  "description": "Test configuration for AddToRosterMode tests",
  "parameters": {
    "CURRENT_NFL_WEEK": 6,
    "NFL_SEASON": 2025,
    "NFL_SCORING_FORMAT": "ppr",
    "NORMALIZATION_MAX_SCALE": 100.0,
    "BASE_BYE_PENALTY": 25.0,
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
def sample_players():
    """Create sample test players with various attributes"""
    players = [
        # QBs
        FantasyPlayer(id=1, name="QB1", team="KC", position="QB", bye_week=7,
                     fantasy_points=250.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=5.0, player_rating=90.0),
        FantasyPlayer(id=2, name="QB2", team="BUF", position="QB", bye_week=10,
                     fantasy_points=220.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=15.0, player_rating=85.0),

        # RBs
        FantasyPlayer(id=3, name="RB1", team="SF", position="RB", bye_week=7,
                     fantasy_points=200.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=3.0, player_rating=92.0),
        FantasyPlayer(id=4, name="RB2", team="PHI", position="RB", bye_week=8,
                     fantasy_points=180.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=10.0, player_rating=88.0),
        FantasyPlayer(id=5, name="RB3", team="DAL", position="RB", bye_week=9,
                     fantasy_points=160.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=25.0, player_rating=80.0),
        FantasyPlayer(id=6, name="RB4", team="MIA", position="RB", bye_week=10,
                     fantasy_points=140.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=40.0, player_rating=75.0),

        # WRs
        FantasyPlayer(id=7, name="WR1", team="MIN", position="WR", bye_week=6,
                     fantasy_points=190.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=8.0, player_rating=89.0),
        FantasyPlayer(id=8, name="WR2", team="CIN", position="WR", bye_week=7,
                     fantasy_points=175.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=18.0, player_rating=86.0),
        FantasyPlayer(id=9, name="WR3", team="DET", position="WR", bye_week=8,
                     fantasy_points=165.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=30.0, player_rating=82.0),
        FantasyPlayer(id=10, name="WR4", team="LAC", position="WR", bye_week=9,
                     fantasy_points=155.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=45.0, player_rating=78.0),

        # TEs
        FantasyPlayer(id=11, name="TE1", team="KC", position="TE", bye_week=7,
                     fantasy_points=145.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=20.0, player_rating=87.0),
        FantasyPlayer(id=12, name="TE2", team="SF", position="TE", bye_week=8,
                     fantasy_points=120.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=50.0, player_rating=74.0),

        # K
        FantasyPlayer(id=13, name="K1", team="BAL", position="K", bye_week=10,
                     fantasy_points=100.0, injury_status="ACTIVE", drafted=0, locked=0,
                     average_draft_position=100.0, player_rating=70.0),

        # DST
        FantasyPlayer(id=14, name="DST1", team="SF", position="DST", bye_week=7,
                     fantasy_points=95.0, injury_status="ACTIVE", drafted=0, locked=0,
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

    # Mock get_player_list to return available players
    def get_player_list_mock(drafted_vals=None, can_draft=False):
        if drafted_vals == [0]:
            return [p for p in sample_players if p.drafted == 0]
        return sample_players

    manager.get_player_list = Mock(side_effect=get_player_list_mock)

    # Mock score_player to return ScoredPlayer
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


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

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


# ============================================================================
# SET MANAGERS TESTS
# ============================================================================

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


# ============================================================================
# GET CURRENT ROUND TESTS
# ============================================================================

class TestGetCurrentRound:
    """Test _get_current_round() method"""

    def test_get_current_round_empty_roster(self, add_to_roster_manager):
        """Test getting current round with empty roster"""
        with patch.object(add_to_roster_manager, '_match_players_to_rounds', return_value={}):
            current_round = add_to_roster_manager._get_current_round()

            assert current_round == 1

    def test_get_current_round_partial_roster(self, add_to_roster_manager):
        """Test getting current round with partial roster"""
        # Simulate 5 players drafted (rounds 1-5 filled)
        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value={1: Mock(), 2: Mock(), 3: Mock(), 4: Mock(), 5: Mock()}):
            current_round = add_to_roster_manager._get_current_round()

            assert current_round == 6

    def test_get_current_round_almost_full_roster(self, add_to_roster_manager):
        """Test getting current round with almost full roster (14/15)"""
        # Simulate 14 players drafted (rounds 1-14 filled)
        filled_rounds = {i: Mock() for i in range(1, 15)}
        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value=filled_rounds):
            current_round = add_to_roster_manager._get_current_round()

            assert current_round == 15

    def test_get_current_round_full_roster(self, add_to_roster_manager):
        """Test getting current round with full roster (15/15)"""
        # Simulate all 15 players drafted
        filled_rounds = {i: Mock() for i in range(1, 16)}
        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value=filled_rounds):
            current_round = add_to_roster_manager._get_current_round()

            # When roster is full, method returns None (no next round)
            assert current_round is None


# ============================================================================
# MATCH PLAYERS TO ROUNDS TESTS
# ============================================================================

class TestMatchPlayersToRounds:
    """Test _match_players_to_rounds() method"""

    def test_match_players_empty_roster(self, add_to_roster_manager, mock_player_manager):
        """Test matching with empty roster"""
        mock_player_manager.team.roster = []

        result = add_to_roster_manager._match_players_to_rounds()

        assert result == {}

    def test_match_players_perfect_match(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test matching when players perfectly match draft order positions"""
        # Round 1 ideal is FLEX, round 3 ideal is QB
        # Put RB in roster (FLEX-eligible) and QB
        rb = sample_players[2]  # RB
        qb = sample_players[0]  # QB
        mock_player_manager.team.roster = [rb, qb]

        result = add_to_roster_manager._match_players_to_rounds()

        # RB should match to round 1 (FLEX), QB to round 3 (QB primary)
        assert 1 in result  # FLEX round
        assert result[1] == rb

    def test_match_players_partial_match(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test matching with partial roster"""
        # Add 3 players that can match to various rounds
        players = [sample_players[2], sample_players[6], sample_players[0]]  # RB, WR, QB
        for p in players:
            p.drafted = 2
        mock_player_manager.team.roster = players

        result = add_to_roster_manager._match_players_to_rounds()

        # Should have matched some players
        assert len(result) > 0
        assert len(result) <= len(players)

    def test_match_players_multiple_same_position(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test matching when multiple players have same position"""
        # Add 4 RBs to roster
        rbs = [sample_players[2], sample_players[3], sample_players[4], sample_players[5]]
        for rb in rbs:
            rb.drafted = 2
        mock_player_manager.team.roster = rbs

        result = add_to_roster_manager._match_players_to_rounds()

        # Multiple RBs should be matched to different FLEX rounds
        assert len(result) > 0

    def test_match_players_uses_optimal_fit(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test that matching uses optimal fit strategy (perfect position match first)"""
        # QB ideally goes to round 3 (QB primary)
        qb = sample_players[0]
        qb.drafted = 2
        mock_player_manager.team.roster = [qb]

        result = add_to_roster_manager._match_players_to_rounds()

        # QB should be matched to a QB-primary round
        assert len(result) > 0
        # Check that QB was matched somewhere
        assert any(p == qb for p in result.values())


# ============================================================================
# GET RECOMMENDATIONS TESTS
# ============================================================================

class TestGetRecommendations:
    """Test get_recommendations() method"""

    def test_get_recommendations_returns_top_players(self, add_to_roster_manager, sample_players):
        """Test that get_recommendations returns top N players"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            recommendations = add_to_roster_manager.get_recommendations()

            # Should return RECOMMENDATION_COUNT players (10)
            assert len(recommendations) == Constants.RECOMMENDATION_COUNT
            # All should be ScoredPlayer objects
            assert all(isinstance(p, ScoredPlayer) for p in recommendations)

    def test_get_recommendations_sorted_by_score(self, add_to_roster_manager, sample_players):
        """Test that recommendations are sorted by score descending"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            recommendations = add_to_roster_manager.get_recommendations()

            # Verify descending order
            for i in range(len(recommendations) - 1):
                assert recommendations[i].score >= recommendations[i+1].score

    def test_get_recommendations_only_available_players(self, add_to_roster_manager, mock_player_manager, sample_players):
        """Test that only available players (drafted=0) are recommended"""
        # Mark some players as drafted
        sample_players[0].drafted = 1  # Drafted by opponent
        sample_players[1].drafted = 2  # On user's roster

        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            recommendations = add_to_roster_manager.get_recommendations()

            # None of the recommended players should be drafted
            for rec in recommendations:
                assert rec.player.drafted == 0

    def test_get_recommendations_only_draftable_players(self, add_to_roster_manager, mock_player_manager):
        """Test that only players that can be drafted are recommended"""
        # get_player_list should be called with can_draft=True
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            add_to_roster_manager.get_recommendations()

            mock_player_manager.get_player_list.assert_called_with(drafted_vals=[0], can_draft=True)

    def test_get_recommendations_uses_draft_round_bonus(self, add_to_roster_manager, mock_player_manager):
        """Test that recommendations use draft_round parameter for bonus"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=5):
            add_to_roster_manager.get_recommendations()

            # score_player should be called with draft_round=5
            # Check that at least one call had draft_round=5
            calls = mock_player_manager.score_player.call_args_list
            assert any(call.kwargs.get('draft_round') == 5 for call in calls)

    def test_get_recommendations_enables_all_scoring_factors(self, add_to_roster_manager, mock_player_manager):
        """Test that all scoring factors are enabled"""
        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            add_to_roster_manager.get_recommendations()

            # Check that score_player was called with all flags True
            calls = mock_player_manager.score_player.call_args_list
            assert len(calls) > 0
            # Check first call has all flags
            first_call = calls[0].kwargs
            assert first_call.get('adp') == True
            assert first_call.get('player_rating') == True
            assert first_call.get('team_quality') == True
            assert first_call.get('performance') == True
            assert first_call.get('matchup') == True

    def test_get_recommendations_empty_when_no_available_players(self, add_to_roster_manager):
        """Test that empty list returned when no available players"""
        # Mock get_player_list on the manager's player_manager to return empty list
        with patch.object(add_to_roster_manager.player_manager, 'get_player_list', return_value=[]):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                recommendations = add_to_roster_manager.get_recommendations()

                assert recommendations == []


# ============================================================================
# DISPLAY ROSTER BY DRAFT ROUNDS TESTS
# ============================================================================

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
        # Add 3 players to roster
        players = sample_players[:3]
        for p in players:
            p.drafted = 2
        mock_player_manager.team.roster = players
        mock_player_manager.get_roster_len.return_value = 3

        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value={1: players[0], 2: players[1], 3: players[2]}):
            add_to_roster_manager._display_roster_by_draft_rounds()

            captured = capsys.readouterr()
            assert "Current Roster by Draft Round:" in captured.out
            assert "Round  1" in captured.out
            assert "[EMPTY SLOT]" in captured.out  # Some rounds should be empty
            assert "Roster Status: 3/15 players drafted" in captured.out

    def test_display_shows_ideal_positions(self, add_to_roster_manager, mock_player_manager, sample_players, capsys):
        """Test that display shows ideal position for each round"""
        # Add at least one player so ideal positions are shown (empty roster returns early)
        players = [sample_players[0]]
        for p in players:
            p.drafted = 2
        mock_player_manager.team.roster = players
        mock_player_manager.get_roster_len.return_value = 1

        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value={1: players[0]}):
            add_to_roster_manager._display_roster_by_draft_rounds()

            captured = capsys.readouterr()
            # Should show ideal positions from DRAFT_ORDER config
            assert "(Ideal:" in captured.out
            assert "FLEX" in captured.out  # FLEX is ideal for many rounds

    def test_display_full_roster(self, add_to_roster_manager, mock_player_manager, sample_players, capsys):
        """Test displaying full roster (15/15)"""
        # Create 15 players for full roster
        full_roster = []
        for i in range(15):
            if i < len(sample_players):
                p = sample_players[i]
            else:
                p = FantasyPlayer(id=100+i, name=f"Extra{i}", team="KC", position="RB",
                                 bye_week=7, fantasy_points=100.0, injury_status="ACTIVE",
                                 drafted=2, locked=0)
            p.drafted = 2
            full_roster.append(p)

        mock_player_manager.team.roster = full_roster
        mock_player_manager.get_roster_len.return_value = 15

        # Mock all rounds filled
        filled_rounds = {i: full_roster[i-1] for i in range(1, 16)}
        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value=filled_rounds):
            add_to_roster_manager._display_roster_by_draft_rounds()

            captured = capsys.readouterr()
            assert "Roster Status: 15/15 players drafted" in captured.out
            # Should not have any [EMPTY SLOT]
            # Count rounds shown
            assert captured.out.count("Round") >= 15


# ============================================================================
# INTERACTIVE MODE TESTS
# ============================================================================

class TestInteractiveMode:
    """Test start_interactive_mode() method"""

    @patch('builtins.input', side_effect=[str(Constants.RECOMMENDATION_COUNT + 1)])  # Choose "Back to Main Menu"
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

    @patch('builtins.input', side_effect=['1'])  # Choose first player
    def test_interactive_mode_draft_player_success(self, mock_input, add_to_roster_manager,
                                                   mock_player_manager, mock_team_data_manager, sample_players, capsys):
        """Test successfully drafting a player"""
        mock_player_manager.get_roster_len.return_value = 0
        mock_player_manager.draft_player.return_value = True

        # Create mock recommendations
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

    @patch('builtins.input', side_effect=['1'])  # Choose first player
    def test_interactive_mode_draft_player_failure(self, mock_input, add_to_roster_manager,
                                                   mock_player_manager, mock_team_data_manager, sample_players, capsys):
        """Test failed player draft"""
        mock_player_manager.get_roster_len.return_value = 0
        mock_player_manager.draft_player.return_value = False  # Draft fails

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

    @patch('builtins.input', side_effect=['abc', '11'])  # Invalid input, then back to menu
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

    @patch('builtins.input', side_effect=['0', '11'])  # Out of range (too low), then back
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
        mock_player_manager.get_roster_len.return_value = 15  # Full roster

        with patch.object(add_to_roster_manager, '_display_roster_by_draft_rounds'):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=None):
                with patch.object(add_to_roster_manager, 'get_recommendations',
                                 return_value=[]):  # No recommendations
                    add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

        captured = capsys.readouterr()
        assert "No recommendations available" in captured.out
        assert "Returning to Main Menu..." in captured.out

    @patch('builtins.input', side_effect=['1'])  # Choose first player
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

        # Verify managers were updated
        assert add_to_roster_manager.player_manager == new_player_manager
        assert add_to_roster_manager.team_data_manager == new_team_manager

    @patch('builtins.input', side_effect=['1'])  # Choose first player
    @patch('builtins.print')  # Mock print to avoid clutter
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

        # Display should be called twice: once at start, once after successful draft
        assert mock_display.call_count == 2


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_get_recommendations_handles_scoring_error(self, add_to_roster_manager, mock_player_manager):
        """Test that get_recommendations handles scoring errors gracefully"""
        # Make score_player raise exception
        mock_player_manager.score_player.side_effect = Exception("Scoring error")

        with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
            # Should raise the exception (not caught in current implementation)
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
                    # KeyboardInterrupt should propagate
                    with pytest.raises(KeyboardInterrupt):
                        add_to_roster_manager.start_interactive_mode(mock_player_manager, mock_team_data_manager)

    def test_match_players_to_rounds_with_duplicate_positions(self, add_to_roster_manager,
                                                              mock_player_manager, sample_players):
        """Test matching when roster has many players of same position"""
        # Add 10 RBs to roster (more than can fit in RB slots)
        rbs = []
        for i in range(10):
            rb = FantasyPlayer(id=100+i, name=f"RB{i}", team="KC", position="RB",
                             bye_week=7, fantasy_points=100.0, injury_status="ACTIVE",
                             drafted=2, locked=0)
            rbs.append(rb)

        mock_player_manager.team.roster = rbs

        result = add_to_roster_manager._match_players_to_rounds()

        # Should match as many as possible (some to RB slots, some to FLEX-primary rounds)
        assert len(result) > 0
        # But not all 10 can be matched (only 15 total rounds)
        assert len(result) <= add_to_roster_manager.config.max_players

    def test_get_current_round_when_roster_is_full(self, add_to_roster_manager):
        """Test _get_current_round returns None when roster is completely full"""
        # All 15 rounds filled
        filled_rounds = {i: Mock() for i in range(1, 16)}

        with patch.object(add_to_roster_manager, '_match_players_to_rounds',
                         return_value=filled_rounds):
            current_round = add_to_roster_manager._get_current_round()

            assert current_round is None

    def test_recommendations_with_single_available_player(self, add_to_roster_manager, sample_players):
        """Test recommendations when only 1 player is available"""
        # Only one player available
        available_player = sample_players[0]
        available_player.drafted = 0

        # Mock get_player_list on the manager's player_manager to return single player
        with patch.object(add_to_roster_manager.player_manager, 'get_player_list', return_value=[available_player]):
            with patch.object(add_to_roster_manager, '_get_current_round', return_value=1):
                recommendations = add_to_roster_manager.get_recommendations()

                # Should return just the one player
                assert len(recommendations) == 1
                assert recommendations[0].player == available_player


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
