"""
Unit tests for SimulatedOpponent module

Tests strategy-based drafting, weekly lineup setting, and roster management.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from simulation.SimulatedOpponent import SimulatedOpponent
from utils.FantasyPlayer import FantasyPlayer


class TestSimulatedOpponentInitialization:
    """Test SimulatedOpponent initialization"""

    def test_init_valid_strategy_adp_aggressive(self):
        """Test initialization with adp_aggressive strategy"""
        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        assert opponent.strategy == SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        assert opponent.projected_pm == projected_pm
        assert opponent.actual_pm == actual_pm
        assert opponent.config == config
        assert opponent.roster == []

    def test_init_valid_strategy_projected_points_aggressive(self):
        """Test initialization with projected_points_aggressive strategy"""
        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_PROJECTED_POINTS_AGGRESSIVE
        )

        assert opponent.strategy == SimulatedOpponent.STRATEGY_PROJECTED_POINTS_AGGRESSIVE

    def test_init_valid_strategy_adp_with_draft_order(self):
        """Test initialization with adp_with_draft_order strategy"""
        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_WITH_DRAFT_ORDER
        )

        assert opponent.strategy == SimulatedOpponent.STRATEGY_ADP_WITH_DRAFT_ORDER

    def test_init_valid_strategy_projected_points_with_draft_order(self):
        """Test initialization with projected_points_with_draft_order strategy"""
        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_PROJECTED_POINTS_WITH_DRAFT_ORDER
        )

        assert opponent.strategy == SimulatedOpponent.STRATEGY_PROJECTED_POINTS_WITH_DRAFT_ORDER

    def test_init_invalid_strategy(self):
        """Test initialization with invalid strategy raises ValueError"""
        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        with pytest.raises(ValueError, match="Invalid strategy"):
            SimulatedOpponent(
                projected_pm, actual_pm, config, team_data_mgr,
                "invalid_strategy"
            )

    def test_init_empty_roster(self):
        """Test that roster starts empty"""
        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        assert len(opponent.roster) == 0


class TestDraftPlayer:
    """Test draft_player functionality"""

    def test_draft_player_adds_to_roster(self):
        """Test that drafting a player adds them to roster"""
        projected_pm = Mock()
        projected_pm.players = []
        actual_pm = Mock()
        actual_pm.players = []
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        player = Mock(spec=FantasyPlayer)
        player.id = 1
        player.name = "Test Player"
        player.position = "RB"

        opponent.draft_player(player)

        assert len(opponent.roster) == 1
        assert opponent.roster[0] == player

    def test_draft_player_marks_drafted_in_projected_pm(self):
        """Test that drafting marks player as drafted=1 in projected PlayerManager"""
        projected_player = Mock(spec=FantasyPlayer)
        projected_player.id = 1
        projected_player.drafted = 0

        projected_pm = Mock()
        projected_pm.players = [projected_player]

        actual_pm = Mock()
        actual_pm.players = []

        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        player = Mock(spec=FantasyPlayer)
        player.id = 1
        player.name = "Test Player"
        player.position = "RB"

        opponent.draft_player(player)

        assert projected_player.drafted == 1

    def test_draft_player_marks_drafted_in_actual_pm(self):
        """Test that drafting marks player as drafted=1 in actual PlayerManager"""
        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = 1
        actual_player.drafted = 0

        projected_pm = Mock()
        projected_pm.players = []

        actual_pm = Mock()
        actual_pm.players = [actual_player]

        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        player = Mock(spec=FantasyPlayer)
        player.id = 1
        player.name = "Test Player"
        player.position = "RB"

        opponent.draft_player(player)

        assert actual_player.drafted == 1

    def test_draft_multiple_players(self):
        """Test drafting multiple players"""
        projected_pm = Mock()
        projected_pm.players = []
        actual_pm = Mock()
        actual_pm.players = []
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        player1 = Mock(spec=FantasyPlayer)
        player1.id = 1
        player1.name = "Player1"
        player1.position = "QB"

        player2 = Mock(spec=FantasyPlayer)
        player2.id = 2
        player2.name = "Player2"
        player2.position = "RB"

        player3 = Mock(spec=FantasyPlayer)
        player3.id = 3
        player3.name = "Player3"
        player3.position = "WR"

        opponent.draft_player(player1)
        opponent.draft_player(player2)
        opponent.draft_player(player3)

        assert len(opponent.roster) == 3
        assert player1 in opponent.roster
        assert player2 in opponent.roster
        assert player3 in opponent.roster


class TestMarkPlayerDrafted:
    """Test mark_player_drafted functionality"""

    def test_mark_player_drafted_in_projected_pm(self):
        """Test marking player as drafted by another team"""
        player = Mock(spec=FantasyPlayer)
        player.id = 5
        player.drafted = 0

        projected_pm = Mock()
        projected_pm.players = [player]

        actual_pm = Mock()
        actual_pm.players = []

        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        opponent.mark_player_drafted(5)

        assert player.drafted == 1

    def test_mark_player_drafted_in_actual_pm(self):
        """Test marking player as drafted in actual PM"""
        player = Mock(spec=FantasyPlayer)
        player.id = 10
        player.drafted = 0

        projected_pm = Mock()
        projected_pm.players = []

        actual_pm = Mock()
        actual_pm.players = [player]

        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        opponent.mark_player_drafted(10)

        assert player.drafted == 1

    def test_mark_player_drafted_nonexistent_player(self):
        """Test marking nonexistent player does nothing"""
        projected_pm = Mock()
        projected_pm.players = []

        actual_pm = Mock()
        actual_pm.players = []

        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        # Should not raise an error
        opponent.mark_player_drafted(999)


class TestGetDraftRecommendation:
    """Test get_draft_recommendation functionality"""

    def test_get_draft_recommendation_no_available_players(self):
        """Test getting recommendation with no available players raises error"""
        projected_pm = Mock()
        projected_pm.players = []

        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        with pytest.raises(ValueError, match="No available players to draft"):
            opponent.get_draft_recommendation()

    @patch('simulation.SimulatedOpponent.random.random')
    def test_adp_aggressive_strategy_picks_lowest_adp(self, mock_random):
        """Test ADP aggressive strategy picks player with lowest ADP"""
        # Mock random to always return 1.0 (no human error)
        mock_random.return_value = 1.0

        player1 = Mock(spec=FantasyPlayer)
        player1.id = 1
        player1.name = "Player1"
        player1.average_draft_position = 10.0
        player1.drafted = 0

        player2 = Mock(spec=FantasyPlayer)
        player2.id = 2
        player2.name = "Player2"
        player2.average_draft_position = 5.0
        player2.drafted = 0

        player3 = Mock(spec=FantasyPlayer)
        player3.id = 3
        player3.name = "Player3"
        player3.average_draft_position = 15.0
        player3.drafted = 0

        projected_pm = Mock()
        projected_pm.players = [player1, player2, player3]

        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        recommendation = opponent.get_draft_recommendation()

        # Should pick player2 (ADP = 5.0, lowest)
        assert recommendation == player2

    @patch('simulation.SimulatedOpponent.random.random')
    def test_projected_points_aggressive_picks_highest_points(self, mock_random):
        """Test projected points aggressive strategy picks highest points"""
        # Mock random to always return 1.0 (no human error)
        mock_random.return_value = 1.0

        player1 = Mock(spec=FantasyPlayer)
        player1.id = 1
        player1.name = "Player1"
        player1.fantasy_points = 100.0
        player1.drafted = 0

        player2 = Mock(spec=FantasyPlayer)
        player2.id = 2
        player2.name = "Player2"
        player2.fantasy_points = 150.0
        player2.drafted = 0

        player3 = Mock(spec=FantasyPlayer)
        player3.id = 3
        player3.name = "Player3"
        player3.fantasy_points = 80.0
        player3.drafted = 0

        projected_pm = Mock()
        projected_pm.players = [player1, player2, player3]

        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_PROJECTED_POINTS_AGGRESSIVE
        )

        recommendation = opponent.get_draft_recommendation()

        # Should pick player2 (150 points, highest)
        assert recommendation == player2

    @patch('simulation.SimulatedOpponent.random.random')
    @patch('simulation.SimulatedOpponent.random.choice')
    def test_human_error_picks_from_top_5(self, mock_choice, mock_random):
        """Test human error causes pick from top 5 instead of #1"""
        # Mock random to always return 0.1 (< 0.2, triggers human error)
        mock_random.return_value = 0.1

        players = []
        for i in range(10):
            player = Mock(spec=FantasyPlayer)
            player.id = i
            player.name = f"Player{i}"
            player.average_draft_position = float(i + 1)
            player.drafted = 0
            players.append(player)

        # Mock choice to return 3rd best player
        mock_choice.return_value = players[2]

        projected_pm = Mock()
        projected_pm.players = players

        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        recommendation = opponent.get_draft_recommendation()

        # Should have called random.choice with top 5 players
        mock_choice.assert_called_once()
        top_5_called = mock_choice.call_args[0][0]
        assert len(top_5_called) == 5

        # Should return the mocked choice (player 2)
        assert recommendation == players[2]


class TestRankingMethods:
    """Test private ranking methods"""

    def test_rank_by_adp_ascending_order(self):
        """Test _rank_by_adp sorts by ADP ascending"""
        player1 = Mock(spec=FantasyPlayer)
        player1.average_draft_position = 20.0

        player2 = Mock(spec=FantasyPlayer)
        player2.average_draft_position = 5.0

        player3 = Mock(spec=FantasyPlayer)
        player3.average_draft_position = 10.0

        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        ranked = opponent._rank_by_adp([player1, player2, player3])

        # Should be sorted by ADP: player2 (5.0), player3 (10.0), player1 (20.0)
        assert ranked[0] == player2
        assert ranked[1] == player3
        assert ranked[2] == player1

    def test_rank_by_projected_points_descending(self):
        """Test _rank_by_projected_points sorts by points descending"""
        player1 = Mock(spec=FantasyPlayer)
        player1.fantasy_points = 100.0

        player2 = Mock(spec=FantasyPlayer)
        player2.fantasy_points = 200.0

        player3 = Mock(spec=FantasyPlayer)
        player3.fantasy_points = 150.0

        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_PROJECTED_POINTS_AGGRESSIVE
        )

        ranked = opponent._rank_by_projected_points([player1, player2, player3])

        # Should be sorted by points desc: player2 (200), player3 (150), player1 (100)
        assert ranked[0] == player2
        assert ranked[1] == player3
        assert ranked[2] == player1

    def test_rank_by_adp_handles_none_values(self):
        """Test _rank_by_adp handles None ADP values"""
        player1 = Mock(spec=FantasyPlayer)
        player1.average_draft_position = 10.0

        player2 = Mock(spec=FantasyPlayer)
        player2.average_draft_position = None

        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        ranked = opponent._rank_by_adp([player1, player2])

        # player1 should be first (has ADP), player2 last (None -> 999.0)
        assert ranked[0] == player1
        assert ranked[1] == player2

    def test_rank_by_projected_points_handles_none_values(self):
        """Test _rank_by_projected_points handles None values"""
        player1 = Mock(spec=FantasyPlayer)
        player1.fantasy_points = 100.0

        player2 = Mock(spec=FantasyPlayer)
        player2.fantasy_points = None

        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_PROJECTED_POINTS_AGGRESSIVE
        )

        ranked = opponent._rank_by_projected_points([player1, player2])

        # player1 should be first (100 points), player2 last (None -> 0.0)
        assert ranked[0] == player1
        assert ranked[1] == player2


class TestRosterAccessors:
    """Test roster accessor methods"""

    def test_get_roster_size_empty(self):
        """Test get_roster_size with empty roster"""
        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        assert opponent.get_roster_size() == 0

    def test_get_roster_size_with_players(self):
        """Test get_roster_size with players"""
        projected_pm = Mock()
        projected_pm.players = []
        actual_pm = Mock()
        actual_pm.players = []
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        player1 = Mock(spec=FantasyPlayer)
        player1.id = 1
        player1.name = "Player1"
        player1.position = "QB"

        player2 = Mock(spec=FantasyPlayer)
        player2.id = 2
        player2.name = "Player2"
        player2.position = "RB"

        opponent.draft_player(player1)
        opponent.draft_player(player2)

        assert opponent.get_roster_size() == 2

    def test_get_roster_players_returns_copy(self):
        """Test get_roster_players returns a copy"""
        projected_pm = Mock()
        projected_pm.players = []
        actual_pm = Mock()
        actual_pm.players = []
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        player = Mock(spec=FantasyPlayer)
        player.id = 1
        player.name = "TestPlayer"
        player.position = "WR"

        opponent.draft_player(player)

        roster_copy = opponent.get_roster_players()

        # Should be equal but not same object
        assert roster_copy == opponent.roster
        assert roster_copy is not opponent.roster

    def test_get_roster_players_empty(self):
        """Test get_roster_players with empty roster"""
        projected_pm = Mock()
        actual_pm = Mock()
        config = Mock()
        team_data_mgr = Mock()

        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, team_data_mgr,
            SimulatedOpponent.STRATEGY_ADP_AGGRESSIVE
        )

        roster = opponent.get_roster_players()

        assert roster == []
        assert len(roster) == 0


class TestConstants:
    """Test class constants"""

    def test_strategy_constants_defined(self):
        """Test that all strategy constants are defined"""
        assert hasattr(SimulatedOpponent, 'STRATEGY_ADP_AGGRESSIVE')
        assert hasattr(SimulatedOpponent, 'STRATEGY_PROJECTED_POINTS_AGGRESSIVE')
        assert hasattr(SimulatedOpponent, 'STRATEGY_ADP_WITH_DRAFT_ORDER')
        assert hasattr(SimulatedOpponent, 'STRATEGY_PROJECTED_POINTS_WITH_DRAFT_ORDER')

    def test_human_error_rate_defined(self):
        """Test that HUMAN_ERROR_RATE constant is defined"""
        assert hasattr(SimulatedOpponent, 'HUMAN_ERROR_RATE')
        assert SimulatedOpponent.HUMAN_ERROR_RATE == 0.2
