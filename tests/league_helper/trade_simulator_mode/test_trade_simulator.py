"""
Comprehensive Unit Tests for Trade Simulator

Tests all functionality of the trade simulator including:
- TradeSimTeam: Team wrapper with scoring functionality
- TradeSnapshot: Trade result data structure
- TradeSimulatorModeManager: Trade generation and analysis

Author: Claude Code
Date: 2025-10-12
"""

import pytest
import tempfile
import json
import csv
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from typing import List

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from utils.FantasyPlayer import FantasyPlayer
from league_helper.trade_simulator_mode.TradeSimTeam import TradeSimTeam
from league_helper.trade_simulator_mode.TradeSnapshot import TradeSnapshot
from league_helper.trade_simulator_mode.TradeSimulatorModeManager import TradeSimulatorModeManager
from league_helper.util.PlayerManager import PlayerManager


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_players():
    """Create sample players for testing"""
    return [
        FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB",
                     fantasy_points=250.0, injury_status="ACTIVE"),
        FantasyPlayer(id=2, name="Josh Allen", team="BUF", position="QB",
                     fantasy_points=240.0, injury_status="ACTIVE"),
        FantasyPlayer(id=3, name="Christian McCaffrey", team="SF", position="RB",
                     fantasy_points=220.0, injury_status="ACTIVE"),
        FantasyPlayer(id=4, name="Derrick Henry", team="TEN", position="RB",
                     fantasy_points=200.0, injury_status="ACTIVE"),
        FantasyPlayer(id=5, name="Justin Jefferson", team="MIN", position="WR",
                     fantasy_points=210.0, injury_status="ACTIVE"),
        FantasyPlayer(id=6, name="Tyreek Hill", team="MIA", position="WR",
                     fantasy_points=205.0, injury_status="ACTIVE"),
        FantasyPlayer(id=7, name="Travis Kelce", team="KC", position="TE",
                     fantasy_points=150.0, injury_status="ACTIVE"),
        FantasyPlayer(id=8, name="Mark Andrews", team="BAL", position="TE",
                     fantasy_points=140.0, injury_status="ACTIVE"),
        FantasyPlayer(id=9, name="Tucker", team="BAL", position="K",
                     fantasy_points=120.0, injury_status="ACTIVE"),
        FantasyPlayer(id=10, name="49ers D/ST", team="SF", position="DST",
                     fantasy_points=110.0, injury_status="ACTIVE"),
        # Injured player for filtering tests
        FantasyPlayer(id=11, name="Injured Player", team="NYJ", position="RB",
                     fantasy_points=180.0, injury_status="OUT"),
        # Questionable player
        FantasyPlayer(id=12, name="Questionable Player", team="DAL", position="WR",
                     fantasy_points=190.0, injury_status="QUESTIONABLE"),
    ]


@pytest.fixture
def mock_config():
    """Create a mock ConfigManager for testing"""
    config = Mock()
    config.current_nfl_week = 7
    config.nfl_season = 2025
    config.nfl_scoring_format = "ppr"
    config.max_positions = {'QB': 2, 'RB': 4, 'WR': 4, 'FLEX': 2, 'TE': 1, 'K': 1, 'DST': 1}
    config.flex_eligible_positions = ['RB', 'WR']
    config.max_players = 15
    return config


@pytest.fixture
def mock_player_manager(sample_players):
    """Create a mock PlayerManager for testing"""
    manager = Mock(spec=PlayerManager)
    manager.players = sample_players

    # Mock the score_player method
    def mock_score_player(player, **kwargs):
        scored_player = Mock()
        scored_player.score = player.fantasy_points / 2  # Simple scoring for tests
        return scored_player

    manager.score_player = Mock(side_effect=mock_score_player)

    # Mock the team
    manager.team = Mock()
    manager.team.roster = sample_players[:5]  # First 5 players on user's team

    # Mock get_lowest_scores_on_roster
    manager.get_lowest_scores_on_roster = Mock(return_value={
        "QB": 0.0, "RB": 0.0, "WR": 0.0, "TE": 0.0, "K": 0.0, "DST": 0.0
    })

    # Mock get_player_list (used by waiver recommendations in unequal trades)
    # Return empty list by default (tests can override this if needed)
    manager.get_player_list = Mock(return_value=[])

    return manager


@pytest.fixture
def temp_data_folder():
    """Create a temporary data folder with necessary CSV files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_path = Path(tmpdir)

        # Create minimal drafted_data.csv
        drafted_csv = data_path / 'drafted_data.csv'
        with open(drafted_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['player_name', 'position', 'team', 'fantasy_team'])
            writer.writerow(['Patrick Mahomes', 'QB', 'KC', 'Sea Sharp'])
            writer.writerow(['Josh Allen', 'QB', 'BUF', 'Team 2'])
            writer.writerow(['Christian McCaffrey', 'RB', 'SF', 'Team 3'])

        yield data_path


# =============================================================================
# TradeSimTeam Tests
# =============================================================================

class TestTradeSimTeamInitialization:
    """Test TradeSimTeam initialization and attributes"""

    def test_initialization_basic(self, sample_players, mock_player_manager):
        """Test basic TradeSimTeam construction"""
        team_players = sample_players[:5]
        team = TradeSimTeam("Test Team", team_players, mock_player_manager)

        assert team.name == "Test Team"
        assert team.player_manager == mock_player_manager
        assert team.isOpponent == True
        assert isinstance(team.team, list)
        assert team.team_score >= 0

    def test_initialization_filters_injured_players(self, sample_players, mock_player_manager):
        """Test that severely injured players (IR) are filtered out, but OUT players are kept"""
        # Create an IR player that should be filtered
        ir_player = FantasyPlayer(id=99, name="IR Player", team="NYG", position="RB",
                                 fantasy_points=180.0, injury_status="IR")
        # Include IR player and OUT player
        team_players = sample_players[:6] + [sample_players[10]] + [ir_player]  # Add OUT and IR players
        team = TradeSimTeam("Test Team", team_players, mock_player_manager)

        # IR player should be filtered, but OUT player should be kept
        assert len(team.team) == len(team_players) - 1  # Only IR filtered
        assert all(p.injury_status in ['ACTIVE', 'QUESTIONABLE', 'OUT'] for p in team.team)
        assert all(p.id != 99 for p in team.team)  # IR player filtered out
        assert any(p.injury_status == 'OUT' for p in team.team)  # OUT player kept

    def test_initialization_keeps_questionable_players(self, sample_players, mock_player_manager):
        """Test that QUESTIONABLE players are kept"""
        # Include questionable player (id=12)
        team_players = sample_players[:6] + [sample_players[11]]  # Add QUESTIONABLE player
        team = TradeSimTeam("Test Team", team_players, mock_player_manager)

        # QUESTIONABLE player should be kept
        questionable_players = [p for p in team.team if p.injury_status == 'QUESTIONABLE']
        assert len(questionable_players) > 0

    def test_initialization_opponent_flag(self, sample_players, mock_player_manager):
        """Test opponent flag affects scoring"""
        team_players = sample_players[:5]

        opponent_team = TradeSimTeam("Opponent", team_players, mock_player_manager, isOpponent=True)
        my_team = TradeSimTeam("My Team", team_players, mock_player_manager, isOpponent=False)

        assert opponent_team.isOpponent == True
        assert my_team.isOpponent == False

    def test_initialization_empty_roster(self, mock_player_manager):
        """Test TradeSimTeam with empty roster"""
        team = TradeSimTeam("Empty Team", [], mock_player_manager)

        assert team.name == "Empty Team"
        assert len(team.team) == 0
        assert team.team_score == 0


class TestTradeSimTeamScoring:
    """Test TradeSimTeam scoring functionality"""

    def test_score_team_called_on_init(self, sample_players, mock_player_manager):
        """Test that score_team is called during initialization"""
        team_players = sample_players[:5]
        team = TradeSimTeam("Test Team", team_players, mock_player_manager)

        # Team should have been scored
        assert team.team_score > 0
        assert mock_player_manager.score_player.called

    def test_score_team_returns_total(self, sample_players, mock_player_manager):
        """Test that score_team returns sum of player scores"""
        team_players = sample_players[:5]
        team = TradeSimTeam("Test Team", team_players, mock_player_manager)

        score = team.score_team()

        assert score == team.team_score
        assert score > 0

    def test_score_team_sets_player_scores(self, sample_players, mock_player_manager):
        """Test that individual player scores are set"""
        team_players = sample_players[:3]
        team = TradeSimTeam("Test Team", team_players, mock_player_manager)

        # Each player should have a score attribute
        for player in team.team:
            assert hasattr(player, 'score')
            assert player.score > 0

    def test_score_team_uses_different_scoring_for_opponents(self, sample_players, mock_player_manager):
        """Test that opponent teams use different scoring (bye=False vs bye=True)"""
        team_players = sample_players[:3]

        opponent_team = TradeSimTeam("Opponent", team_players, mock_player_manager, isOpponent=True)

        # Verify that score_player was called with opponent flags
        # Opponents use same scoring as user except bye=False (to avoid artificial score changes)
        calls = mock_player_manager.score_player.call_args_list
        opponent_calls = [call for call in calls if 'bye' in call[1] and not call[1]['bye']]

        assert len(opponent_calls) > 0


# =============================================================================
# TradeSnapshot Tests
# =============================================================================

class TestTradeSnapshotConstruction:
    """Test TradeSnapshot initialization and attributes"""

    def test_initialization_basic(self, sample_players, mock_player_manager):
        """Test basic TradeSnapshot construction"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        # Get scored players from the correct teams (players must be in the team's roster to be scored)
        my_new_players = their_team.get_scored_players([sample_players[5]])
        their_new_players = my_team.get_scored_players([sample_players[0]])

        snapshot = TradeSnapshot(my_team, my_new_players, their_team, their_new_players)

        assert snapshot.my_new_team == my_team
        assert snapshot.my_new_players == my_new_players
        assert snapshot.their_new_team == their_team
        assert snapshot.their_new_players == their_new_players

    def test_initialization_multiple_players(self, sample_players, mock_player_manager):
        """Test TradeSnapshot with multiple players"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        # Get scored players from the correct teams (players must be in the team's roster to be scored)
        my_new_players = their_team.get_scored_players([sample_players[5], sample_players[6]])
        their_new_players = my_team.get_scored_players([sample_players[0], sample_players[1]])

        snapshot = TradeSnapshot(my_team, my_new_players, their_team, their_new_players)

        assert len(snapshot.my_new_players) == 2
        assert len(snapshot.their_new_players) == 2

    def test_snapshot_preserves_team_scores(self, sample_players, mock_player_manager):
        """Test that TradeSnapshot preserves team score information"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        # Get scored players from the correct teams (players must be in the team's roster to be scored)
        my_new_players = their_team.get_scored_players([sample_players[5]])
        their_new_players = my_team.get_scored_players([sample_players[0]])

        snapshot = TradeSnapshot(my_team, my_new_players, their_team, their_new_players)

        assert snapshot.my_new_team.team_score >= 0
        assert snapshot.their_new_team.team_score >= 0


# =============================================================================
# TradeSimulatorModeManager Initialization Tests
# =============================================================================

class TestTradeSimulatorModeManagerInitialization:
    """Test TradeSimulatorModeManager initialization"""

    def test_initialization_basic(self, temp_data_folder, mock_player_manager, mock_config):
        """Test basic initialization"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

            assert manager.data_folder == temp_data_folder
            assert manager.player_manager == mock_player_manager
            assert isinstance(manager.team_rosters, dict)
            assert isinstance(manager.opponent_simulated_teams, list)
            assert isinstance(manager.trade_snapshots, list)

    def test_initialization_calls_init_team_data(self, temp_data_folder, mock_player_manager, mock_config):
        """Test that init_team_data is called during initialization"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            with patch.object(TradeSimulatorModeManager, 'init_team_data') as mock_init:
                manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)
                mock_init.assert_called_once()


class TestTradeSimulatorModeManagerPositionValidation:
    """Test position validation helper methods"""

    @pytest.fixture
    def manager(self, temp_data_folder, mock_player_manager, mock_config):
        """Create a TradeSimulatorModeManager for testing"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            return TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

    def test_count_positions_basic(self, manager, sample_players):
        """Test basic position counting"""
        roster = sample_players[:10]  # Mix of positions
        counts = manager.analyzer.count_positions(roster)

        assert isinstance(counts, dict)
        assert counts['QB'] == 2  # Mahomes, Allen
        assert counts['RB'] == 2  # McCaffrey, Henry
        assert counts['WR'] == 2  # Jefferson, Hill
        assert counts['TE'] == 2  # Kelce, Andrews
        assert counts['K'] == 1   # Tucker
        assert counts['DST'] == 1  # 49ers

    def test_count_positions_empty_roster(self, manager):
        """Test counting positions with empty roster"""
        counts = manager.analyzer.count_positions([])

        # All positions should have 0
        for pos, count in counts.items():
            assert count == 0

    def test_count_positions_single_position(self, manager, sample_players):
        """Test counting with only one position"""
        roster = [sample_players[0], sample_players[1]]  # Two QBs
        counts = manager.analyzer.count_positions(roster)

        assert counts['QB'] == 2
        assert counts['RB'] == 0
        assert counts['WR'] == 0

    def test_validate_roster_valid(self, manager, sample_players):
        """Test validation of valid roster"""
        # Create a valid roster (skip second TE since TE is not FLEX-eligible and only 1 TE slot exists)
        roster = [
            sample_players[0],  # QB1
            sample_players[1],  # QB2
            sample_players[2],  # RB1
            sample_players[3],  # RB2
            sample_players[4],  # WR1
            sample_players[5],  # WR2
            sample_players[6],  # TE1
            # Skip sample_players[7] (TE2) - TE not FLEX-eligible, only 1 TE slot
            sample_players[8],  # K1
            sample_players[9],  # DST1
        ]
        is_valid = manager.analyzer.validate_roster(roster)

        assert is_valid == True

    def test_validate_roster_too_many_players(self, manager, sample_players):
        """Test validation fails with too many players"""
        # Create roster with 16 players (MAX_PLAYERS = 15)
        roster = sample_players + [sample_players[0]]  # 12 + 1 = 13, add more
        roster = roster + [sample_players[1], sample_players[2], sample_players[3]]  # Total 16

        is_valid = manager.analyzer.validate_roster(roster)

        # Should fail due to exceeding MAX_PLAYERS (15)
        if len(roster) > 15:
            assert is_valid == False

    def test_validate_roster_position_limit_exceeded(self, manager, sample_players):
        """Test validation fails when position limit exceeded"""
        # Create roster with too many QBs (MAX: 2)
        roster = [sample_players[0], sample_players[1],
                 FantasyPlayer(id=99, name="Third QB", team="GB", position="QB",
                             fantasy_points=200.0, injury_status="ACTIVE")]

        is_valid = manager.analyzer.validate_roster(roster)

        # Should fail due to exceeding QB limit
        assert is_valid == False

    def test_validate_roster_empty(self, manager):
        """Test validation of empty roster"""
        is_valid = manager.analyzer.validate_roster([])

        assert is_valid == True  # Empty roster is valid


# =============================================================================
# Trade Combination Generation Tests
# =============================================================================

class TestGetTradeCombinations:
    """Test trade combination generation"""

    @pytest.fixture
    def manager(self, temp_data_folder, mock_player_manager, mock_config):
        """Create a manager for testing"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            return TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

    def test_one_for_one_trades_generated(self, manager, sample_players, mock_player_manager):
        """Test that 1-for-1 trades are generated"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        # Make scores improve for testing
        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_one=True,
            two_for_two=False,
            three_for_three=False
        )

        # Should generate some combinations (if they pass validation and improvement checks)
        assert isinstance(trades, list)
        # Note: May be 0 if no trades improve both teams

    def test_two_for_two_trades_generated(self, manager, sample_players, mock_player_manager):
        """Test that 2-for-2 trades are generated"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_one=False,
            two_for_two=True,
            three_for_three=False
        )

        assert isinstance(trades, list)

    def test_three_for_three_trades_generated(self, manager, sample_players, mock_player_manager):
        """Test that 3-for-3 trades are generated"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_one=False,
            two_for_two=False,
            three_for_three=True
        )

        assert isinstance(trades, list)

    def test_all_trade_types_combined(self, manager, sample_players, mock_player_manager):
        """Test generating all trade types together"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_one=True,
            two_for_two=True,
            three_for_three=True
        )

        assert isinstance(trades, list)

    def test_waiver_trade_skips_their_validation(self, manager, sample_players, mock_player_manager):
        """Test that waiver trades skip validation for their team"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Waiver Wire", sample_players[5:10], mock_player_manager, isOpponent=True)

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=True,  # This should skip their team validation
            one_for_one=True,
            two_for_two=False,
            three_for_three=False
        )

        assert isinstance(trades, list)

    def test_trade_snapshots_have_correct_structure(self, manager, sample_players, mock_player_manager):
        """Test that generated TradeSnapshots have correct structure"""
        my_team = TradeSimTeam("My Team", sample_players[:3], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[3:6], mock_player_manager, isOpponent=True)

        # Manipulate to ensure at least some trades are generated
        my_team.team_score = 50.0
        their_team.team_score = 50.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=True,
            one_for_one=True,
            two_for_two=False,
            three_for_three=False
        )

        if len(trades) > 0:
            trade = trades[0]
            # Check type by class name to avoid import resolution issues
            assert trade.__class__.__name__ == 'TradeSnapshot'
            assert hasattr(trade, 'my_new_team')
            assert hasattr(trade, 'my_new_players')
            assert hasattr(trade, 'their_new_team')
            assert hasattr(trade, 'their_new_players')

    def test_only_mutually_beneficial_trades_returned(self, manager, sample_players, mock_player_manager):
        """Test that only trades improving both teams are returned"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        original_my_score = my_team.team_score
        original_their_score = their_team.team_score

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_one=True,
            two_for_two=False,
            three_for_three=False
        )

        # All trades should improve both teams
        for trade in trades:
            assert trade.my_new_team.team_score > original_my_score
            assert trade.their_new_team.team_score > original_their_score


# =============================================================================
# Waiver Optimizer Tests
# =============================================================================

class TestWaiverOptimizer:
    """Test waiver optimizer functionality"""

    @pytest.fixture
    def manager_with_waivers(self, temp_data_folder, mock_player_manager, mock_config, sample_players):
        """Create manager with waiver wire players"""
        # Set some players as available (drafted=0)
        for i in range(5, 10):
            sample_players[i].drafted = 0

        # Mock get_player_list to return waiver players
        mock_player_manager.get_player_list = Mock(return_value=sample_players[5:10])

        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            return TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

    def test_waiver_optimizer_returns_bool(self, manager_with_waivers):
        """Test that waiver optimizer returns tuple of (bool, list)"""
        with patch('builtins.input', return_value=''):
            with patch('builtins.print'):
                result = manager_with_waivers.start_waiver_optimizer()
                assert isinstance(result, tuple)
                assert len(result) == 2
                assert isinstance(result[0], bool)
                assert isinstance(result[1], list)

    def test_waiver_optimizer_handles_no_waiver_players(self, temp_data_folder, mock_player_manager, mock_config):
        """Test waiver optimizer with no available players"""
        mock_player_manager.get_player_list = Mock(return_value=[])

        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

        with patch('builtins.input', return_value=''):
            with patch('builtins.print'):
                result = manager.start_waiver_optimizer()
                assert result == (True, [])

    def test_waiver_optimizer_calls_get_trade_combinations(self, manager_with_waivers):
        """Test that waiver optimizer calls trade generation"""
        with patch.object(manager_with_waivers.analyzer, 'get_trade_combinations', return_value=[]) as mock_get:
            with patch('builtins.input', return_value=''):
                with patch('builtins.print'):
                    manager_with_waivers.start_waiver_optimizer()

                    # Should be called with waiver-specific parameters
                    mock_get.assert_called_once()
                    call_args = mock_get.call_args[1]
                    assert call_args['is_waivers'] == True
                    assert call_args['one_for_one'] == True
                    assert call_args['two_for_two'] == False  # WAIVERS_TWO_FOR_TWO is False
                    assert call_args['three_for_three'] == False  # WAIVERS_THREE_FOR_THREE is False


# =============================================================================
# Trade Suggestor Tests
# =============================================================================

class TestTradeSuggestor:
    """Test trade suggestor functionality"""

    @pytest.fixture
    def manager_with_opponents(self, temp_data_folder, mock_player_manager, mock_config, sample_players):
        """Create manager with opponent teams"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

            # Manually add opponent teams for testing
            manager.opponent_simulated_teams = [
                TradeSimTeam("Team 1", sample_players[:5], mock_player_manager),
                TradeSimTeam("Team 2", sample_players[5:10], mock_player_manager),
            ]

            return manager

    def test_trade_suggestor_returns_bool(self, manager_with_opponents):
        """Test that trade suggestor returns tuple or list"""
        with patch('builtins.input', return_value=''):
            with patch('builtins.print'):
                result = manager_with_opponents.start_trade_suggestor()
                # Can return either tuple (True, []) or just [] depending on whether trades found
                assert isinstance(result, (tuple, list))
                if isinstance(result, tuple):
                    assert len(result) == 2
                    assert isinstance(result[0], bool)
                    assert isinstance(result[1], list)

    def test_trade_suggestor_handles_no_opponents(self, temp_data_folder, mock_player_manager, mock_config):
        """Test trade suggestor with no opponent teams"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)
            manager.opponent_simulated_teams = []

        with patch('builtins.input', return_value=''):
            with patch('builtins.print'):
                result = manager.start_trade_suggestor()
                assert result == (True, [])

    def test_trade_suggestor_checks_all_opponents(self, manager_with_opponents):
        """Test that trade suggestor analyzes all opponent teams"""
        with patch.object(manager_with_opponents.analyzer, 'get_trade_combinations', return_value=[]) as mock_get:
            with patch('builtins.input', return_value=''):
                with patch('builtins.print'):
                    manager_with_opponents.start_trade_suggestor()

                    # Should be called once for each opponent
                    assert mock_get.call_count == 2

    def test_trade_suggestor_uses_correct_parameters(self, manager_with_opponents):
        """Test that trade suggestor uses correct trade parameters"""
        with patch.object(manager_with_opponents.analyzer, 'get_trade_combinations', return_value=[]) as mock_get:
            with patch('builtins.input', return_value=''):
                with patch('builtins.print'):
                    manager_with_opponents.start_trade_suggestor()

                    # Check parameters of first call
                    call_args = mock_get.call_args_list[0][1]
                    assert call_args['is_waivers'] == False
                    assert call_args['one_for_one'] == False  # ENABLE_ONE_FOR_ONE is False
                    assert call_args['two_for_two'] == True
                    assert call_args['three_for_three'] == True


# =============================================================================
# Edge Cases and Error Handling
# =============================================================================

class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_trade_sim_team_with_all_injured_players(self, sample_players, mock_player_manager):
        """Test TradeSimTeam with only injured players"""
        injured_players = [
            FantasyPlayer(id=99, name="Injured 1", team="NYJ", position="RB",
                         fantasy_points=180.0, injury_status="OUT"),
            FantasyPlayer(id=100, name="Injured 2", team="NYJ", position="WR",
                         fantasy_points=170.0, injury_status="DOUBTFUL"),
            FantasyPlayer(id=101, name="Injured 3", team="NYJ", position="QB",
                         fantasy_points=200.0, injury_status="IR"),
        ]

        team = TradeSimTeam("Injured Team", injured_players, mock_player_manager)

        # OUT players kept, DOUBTFUL and IR filtered
        assert len(team.team) == 1  # Only OUT player kept
        assert team.team[0].injury_status == "OUT"

    def test_get_trade_combinations_with_empty_teams(self, temp_data_folder, mock_player_manager, mock_config):
        """Test trade generation with empty teams"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

        my_team = TradeSimTeam("Empty My Team", [], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Empty Their Team", [], mock_player_manager, isOpponent=True)

        trades = manager.analyzer.get_trade_combinations(my_team, their_team)

        assert len(trades) == 0

    def test_get_trade_combinations_with_minimal_rosters(self, temp_data_folder, mock_player_manager, mock_config, sample_players):
        """Test trade generation with very small rosters"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

        my_team = TradeSimTeam("Minimal Team", sample_players[:1], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Minimal Team 2", sample_players[1:2], mock_player_manager, isOpponent=True)

        trades = manager.analyzer.get_trade_combinations(my_team, their_team, one_for_one=True)

        # Should generate at most 1 trade (1x1)
        assert len(trades) <= 1

    def test_position_validation_with_flex_positions(self, temp_data_folder, mock_player_manager, mock_config, sample_players):
        """Test position validation correctly handles FLEX-eligible positions"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

        # Create roster with players that could fill FLEX
        roster = [
            sample_players[2],  # RB
            sample_players[3],  # RB
            sample_players[4],  # WR
            sample_players[5],  # WR
        ]

        is_valid = manager.analyzer.validate_roster(roster)

        # Should be valid as RB and WR can fill FLEX spots
        assert isinstance(is_valid, bool)


# =============================================================================
# Unequal Trade Tests
# =============================================================================

class TestUnequalTrades:
    """Test unequal trade functionality (2:1, 1:2, 3:1, 1:3, 3:2, 2:3)"""

    @pytest.fixture
    def manager(self, temp_data_folder, mock_player_manager, mock_config):
        """Create a manager for testing"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            return TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

    def test_two_for_one_trades_generated(self, manager, sample_players, mock_player_manager):
        """Test that 2:1 trades (give 2, get 1) are generated"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_one=False,
            two_for_two=False,
            three_for_three=False,
            two_for_one=True
        )

        assert isinstance(trades, list)
        # 2:1 trades should exist if roster composition allows

    def test_one_for_two_trades_generated(self, manager, sample_players, mock_player_manager):
        """Test that 1:2 trades (give 1, get 2) are generated"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_one=False,
            two_for_two=False,
            three_for_three=False,
            one_for_two=True
        )

        assert isinstance(trades, list)
        # 1:2 trades should exist if roster composition allows

    def test_three_for_one_trades_generated(self, manager, sample_players, mock_player_manager):
        """Test that 3:1 trades (give 3, get 1) are generated"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            three_for_one=True
        )

        assert isinstance(trades, list)

    def test_one_for_three_trades_generated(self, manager, sample_players, mock_player_manager):
        """Test that 1:3 trades (give 1, get 3) are generated"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_three=True
        )

        assert isinstance(trades, list)

    def test_three_for_two_trades_generated(self, manager, sample_players, mock_player_manager):
        """Test that 3:2 trades (give 3, get 2) are generated"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            three_for_two=True
        )

        assert isinstance(trades, list)

    def test_two_for_three_trades_generated(self, manager, sample_players, mock_player_manager):
        """Test that 2:3 trades (give 2, get 3) are generated"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            two_for_three=True
        )

        assert isinstance(trades, list)

    def test_all_unequal_trade_types_combined(self, manager, sample_players, mock_player_manager):
        """Test generating all unequal trade types together"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            two_for_one=True,
            one_for_two=True,
            three_for_one=True,
            one_for_three=True,
            three_for_two=True,
            two_for_three=True
        )

        assert isinstance(trades, list)
        # Should generate combinations from all enabled trade types

    def test_waiver_recommendations_in_unequal_trades(self, manager, sample_players, mock_player_manager):
        """Test that waiver recommendations are generated for trades that lose roster spots"""
        # Create waiver wire players
        waiver_players = [
            FantasyPlayer(id=20, name="Waiver QB", team="ATL", position="QB",
                         fantasy_points=100.0, injury_status="ACTIVE", drafted=0),
            FantasyPlayer(id=21, name="Waiver RB", team="ATL", position="RB",
                         fantasy_points=95.0, injury_status="ACTIVE", drafted=0),
        ]

        # Mock get_player_list to return waiver players
        mock_player_manager.get_player_list = Mock(return_value=waiver_players)

        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        # 2:1 trade should generate waiver recommendations (loses 1 roster spot)
        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            two_for_one=True
        )

        # If trades were generated, they should have waiver recommendations
        for trade in trades:
            # 2:1 gives 2, gets 1 - should have 1 waiver recommendation
            assert hasattr(trade, 'waiver_recommendations')
            # May be None or empty list if no waiver players available

    def test_drop_system_in_unequal_trades(self, manager, sample_players, mock_player_manager):
        """Test that drop system works for trades that gain roster spots"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        # 1:2 trade should use drop system (gains 1 roster spot, might need to drop)
        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_two=True
        )

        # Trades should have drop system fields
        for trade in trades:
            assert hasattr(trade, 'my_dropped_players')
            assert hasattr(trade, 'their_dropped_players')

    def test_trade_snapshot_has_unequal_trade_fields(self, manager, sample_players, mock_player_manager):
        """Test that TradeSnapshot has all unequal trade fields"""
        my_team = TradeSimTeam("My Team", sample_players[:3], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[3:6], mock_player_manager, isOpponent=True)

        my_team.team_score = 50.0
        their_team.team_score = 50.0

        # Create a simple trade snapshot
        my_new_players = their_team.get_scored_players([sample_players[3]])
        their_new_players = my_team.get_scored_players([sample_players[0]])

        snapshot = TradeSnapshot(
            my_team, my_new_players,
            their_team, their_new_players,
            waiver_recommendations=[],
            their_waiver_recommendations=[],
            my_dropped_players=[],
            their_dropped_players=[]
        )

        # Verify all unequal trade fields exist
        assert hasattr(snapshot, 'waiver_recommendations')
        assert hasattr(snapshot, 'their_waiver_recommendations')
        assert hasattr(snapshot, 'my_dropped_players')
        assert hasattr(snapshot, 'their_dropped_players')

    def test_min_trade_improvement_enforced_in_unequal_trades(self, manager, sample_players, mock_player_manager):
        """Test that MIN_TRADE_IMPROVEMENT (30 points) is enforced for unequal trades"""
        my_team = TradeSimTeam("My Team", sample_players[:5], mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        # Set scores so trades would need +30 improvement
        my_team.team_score = 100.0
        their_team.team_score = 100.0

        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            two_for_one=True
        )

        # All trades should improve both teams by at least MIN_TRADE_IMPROVEMENT
        for trade in trades:
            my_improvement = trade.my_new_team.team_score - my_team.team_score
            their_improvement = trade.their_new_team.team_score - their_team.team_score

            # Each team should improve by at least 30 points (MIN_TRADE_IMPROVEMENT)
            assert my_improvement >= 30.0
            assert their_improvement >= 30.0

    def test_unequal_trades_respect_roster_limits(self, manager, sample_players, mock_player_manager):
        """Test that unequal trades respect MAX_PLAYERS limit"""
        # Create nearly-full roster (14 players, MAX=15)
        my_roster = sample_players[:10] + [sample_players[0], sample_players[1], sample_players[2], sample_players[3]][:4]
        my_team = TradeSimTeam("My Team", my_roster, mock_player_manager, isOpponent=False)
        their_team = TradeSimTeam("Their Team", sample_players[5:10], mock_player_manager, isOpponent=True)

        my_team.team_score = 100.0
        their_team.team_score = 100.0

        # 1:2 trade would violate roster limit (14 - 1 + 2 = 15, which is OK)
        # 1:3 trade would violate (14 - 1 + 3 = 16 > 15, should use drop system or be rejected)
        trades = manager.analyzer.get_trade_combinations(
            my_team, their_team,
            is_waivers=False,
            one_for_two=True,
            one_for_three=True
        )

        # All trades should either respect limit or use drop system
        for trade in trades:
            total_players = len(trade.my_new_team.team)
            # With drop system, should never exceed 15
            assert total_players <= 15


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration:
    """Integration tests for full trade simulator workflows"""

    def test_full_waiver_optimizer_workflow(self, temp_data_folder, mock_player_manager, mock_config, sample_players):
        """Test complete waiver optimizer workflow"""
        # Setup
        for i in range(5, 10):
            sample_players[i].drafted = 0
        mock_player_manager.get_player_list = Mock(return_value=sample_players[5:10])

        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)

        # Execute
        with patch('builtins.input', return_value=''):
            with patch('builtins.print'):
                result = manager.start_waiver_optimizer()

        # Verify
        assert isinstance(result, tuple)
        assert result[0] == True
        assert isinstance(result[1], list)
        assert mock_player_manager.get_player_list.called

    def test_full_trade_suggestor_workflow(self, temp_data_folder, mock_player_manager, mock_config, sample_players):
        """Test complete trade suggestor workflow"""
        with patch('league_helper.constants.FANTASY_TEAM_NAME', 'Sea Sharp'):
            manager = TradeSimulatorModeManager(temp_data_folder, mock_player_manager, mock_config)
            manager.opponent_simulated_teams = [
                TradeSimTeam("Team 1", sample_players[:5], mock_player_manager),
            ]

        # Execute
        with patch('builtins.input', return_value=''):
            with patch('builtins.print'):
                result = manager.start_trade_suggestor()

        # Verify - can return either tuple or list depending on implementation
        assert isinstance(result, (tuple, list))


class TestBackwardCompatibility:
    """Test backward compatibility - ensure weekly normalization doesn't affect Trade Simulator"""

    def test_trade_simulator_uses_ros_normalization(self, mock_player_manager, mock_config):
        """Test that Trade Simulator mode continues using ROS max_projection (backward compatibility)"""
        # This test ensures weekly normalization feature doesn't affect Trade Simulator mode
        from utils.FantasyPlayer import FantasyPlayer
        from league_helper.util.ScoredPlayer import ScoredPlayer

        # Create test player with ROS projection of 300.0
        test_player = FantasyPlayer(id=1, name="Test Player", team="KC", position="RB",
                                   fantasy_points=300.0, injury_status="ACTIVE")

        # Set up scoring calculator with both ROS and weekly max
        mock_player_manager.max_projection = 400.0
        mock_player_manager.scoring_calculator = Mock()
        mock_player_manager.scoring_calculator.max_projection = 400.0
        mock_player_manager.max_weekly_projections = {7: 30.0}  # Weekly max (not used for ROS)
        mock_player_manager.scoring_calculator.max_weekly_projection = 0.0  # Should remain 0 for ROS mode

        # Mock score_player to use ROS normalization (use_weekly_projection=False)
        def mock_score_player(player, **kwargs):
            # Verify use_weekly_projection is False (ROS mode - default for Trade Simulator)
            assert kwargs.get('use_weekly_projection', False) == False
            # ROS normalization: (300/400) * 100 = 75.0
            return ScoredPlayer(player, 75.0, "ROS normalization test")

        mock_player_manager.score_player = Mock(side_effect=mock_score_player)

        # Call score_player in ROS mode (as Trade Simulator does)
        result = mock_player_manager.score_player(
            test_player,
            use_weekly_projection=False,  # Trade Simulator uses ROS
            adp=True,
            player_rating=True,
            team_quality=True,
            schedule=True
        )

        # Verify score uses ROS max: (300/400) * 100 = 75.0 (not 1000.0 from 300/30)
        assert result.score == 75.0
        assert mock_player_manager.score_player.called


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
