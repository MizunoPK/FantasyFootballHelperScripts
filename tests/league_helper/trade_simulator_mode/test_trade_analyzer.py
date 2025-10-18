"""
Tests for TradeAnalyzer class

Tests trade analysis, roster validation, and trade combination generation.
Covers position counting, roster validation logic, and trade scenario generation.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from league_helper.trade_simulator_mode.trade_analyzer import TradeAnalyzer
from league_helper.trade_simulator_mode.TradeSimTeam import TradeSimTeam
from league_helper.trade_simulator_mode.TradeSnapshot import TradeSnapshot


@pytest.fixture
def mock_player_manager():
    """Create a mock PlayerManager"""
    return Mock()


@pytest.fixture
def mock_config():
    """Create a mock ConfigManager"""
    return Mock()


@pytest.fixture
def analyzer(mock_player_manager, mock_config):
    """Create a TradeAnalyzer instance with mocked dependencies"""
    return TradeAnalyzer(mock_player_manager, mock_config)


@pytest.fixture
def sample_players():
    """Create sample FantasyPlayer objects for testing"""
    qb1 = FantasyPlayer(id=1, name="QB1", team="KC", position="QB", fantasy_points=25.0)
    qb1.locked = 0
    rb1 = FantasyPlayer(id=2, name="RB1", team="SF", position="RB", fantasy_points=20.0)
    rb1.locked = 0
    rb2 = FantasyPlayer(id=3, name="RB2", team="BUF", position="RB", fantasy_points=18.0)
    rb2.locked = 0
    wr1 = FantasyPlayer(id=4, name="WR1", team="MIA", position="WR", fantasy_points=22.0)
    wr1.locked = 0
    wr2 = FantasyPlayer(id=5, name="WR2", team="DAL", position="WR", fantasy_points=19.0)
    wr2.locked = 0
    te1 = FantasyPlayer(id=6, name="TE1", team="KC", position="TE", fantasy_points=15.0)
    te1.locked = 0
    k1 = FantasyPlayer(id=7, name="K1", team="BAL", position="K", fantasy_points=10.0)
    k1.locked = 0
    dst1 = FantasyPlayer(id=8, name="DST1", team="PIT", position="DST", fantasy_points=12.0)
    dst1.locked = 0

    return {
        'qb1': qb1, 'rb1': rb1, 'rb2': rb2, 'wr1': wr1,
        'wr2': wr2, 'te1': te1, 'k1': k1, 'dst1': dst1
    }


class TestTradeAnalyzerInitialization:
    """Test TradeAnalyzer class initialization"""

    def test_class_initialization(self, mock_player_manager, mock_config):
        """Test that TradeAnalyzer initializes correctly"""
        analyzer = TradeAnalyzer(mock_player_manager, mock_config)
        assert analyzer is not None
        assert analyzer.player_manager == mock_player_manager
        assert analyzer.config == mock_config

    def test_initialization_stores_dependencies(self, analyzer, mock_player_manager, mock_config):
        """Test that initialization stores player_manager and config"""
        assert hasattr(analyzer, 'player_manager')
        assert hasattr(analyzer, 'config')
        assert analyzer.player_manager is mock_player_manager
        assert analyzer.config is mock_config


class TestCountPositions:
    """Test count_positions method"""

    def test_count_empty_roster(self, analyzer):
        """Test counting positions in an empty roster"""
        result = analyzer.count_positions([])
        assert isinstance(result, dict)
        # All positions should be 0
        assert all(count == 0 for count in result.values())

    def test_count_single_position(self, analyzer, sample_players):
        """Test counting roster with single position"""
        roster = [sample_players['qb1']]
        result = analyzer.count_positions(roster)
        assert result['QB'] == 1
        assert result['RB'] == 0
        assert result['WR'] == 0

    def test_count_multiple_positions(self, analyzer, sample_players):
        """Test counting roster with multiple positions"""
        roster = [sample_players['qb1'], sample_players['rb1'], sample_players['wr1']]
        result = analyzer.count_positions(roster)
        assert result['QB'] == 1
        assert result['RB'] == 1
        assert result['WR'] == 1
        assert result['TE'] == 0

    def test_count_multiple_same_position(self, analyzer, sample_players):
        """Test counting roster with multiple players at same position"""
        roster = [sample_players['rb1'], sample_players['rb2']]
        result = analyzer.count_positions(roster)
        assert result['RB'] == 2
        assert result['QB'] == 0

    def test_count_all_positions(self, analyzer, sample_players):
        """Test counting roster with all standard positions"""
        roster = [
            sample_players['qb1'],
            sample_players['rb1'],
            sample_players['wr1'],
            sample_players['te1'],
            sample_players['k1'],
            sample_players['dst1']
        ]
        result = analyzer.count_positions(roster)
        assert result['QB'] == 1
        assert result['RB'] == 1
        assert result['WR'] == 1
        assert result['TE'] == 1
        assert result['K'] == 1
        assert result['DST'] == 1


class TestValidateRoster:
    """Test validate_roster method"""

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_validate_valid_roster(self, analyzer, sample_players, mock_config):
        """Test validating a valid roster"""
        roster = [sample_players['qb1'], sample_players['rb1'], sample_players['wr1']]

        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            mock_instance.draft_player = Mock(return_value=True)
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster(roster)
            assert result is True

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 2)
    def test_validate_roster_exceeds_max_players(self, analyzer, sample_players):
        """Test that roster exceeding MAX_PLAYERS is invalid"""
        roster = [sample_players['qb1'], sample_players['rb1'], sample_players['wr1']]
        result = analyzer.validate_roster(roster)
        assert result is False

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 2)
    def test_validate_roster_with_ignore_max_positions(self, analyzer, sample_players):
        """Test that ignore_max_positions allows roster over limit for positions but not total"""
        roster = [sample_players['qb1'], sample_players['rb1'], sample_players['wr1']]
        # Should still fail because total roster size (3) > MAX_PLAYERS (2)
        result = analyzer.validate_roster(roster, ignore_max_positions=True)
        assert result is False

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 5)
    def test_validate_roster_ignores_position_limits_when_flag_set(self, analyzer, sample_players):
        """Test that ignore_max_positions skips position validation"""
        roster = [sample_players['qb1'], sample_players['rb1']]
        # With ignore flag, should only check roster size
        result = analyzer.validate_roster(roster, ignore_max_positions=True)
        assert result is True

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_validate_empty_roster(self, analyzer):
        """Test validating an empty roster"""
        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster([])
            assert result is True

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_validate_roster_at_max_boundary(self, analyzer, sample_players):
        """Test validating roster at exact MAX_PLAYERS boundary"""
        # Create roster with exactly MAX_PLAYERS (15)
        roster = [sample_players['qb1']] * 15

        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            mock_instance.draft_player = Mock(return_value=True)
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster(roster)
            assert result is True

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_validate_roster_with_position_violation(self, analyzer, sample_players):
        """Test that roster with position violations is invalid"""
        roster = [sample_players['qb1'], sample_players['rb1']]

        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            # First player drafts successfully, second fails
            mock_instance.draft_player = Mock(side_effect=[True, False])
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster(roster)
            assert result is False

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_validate_roster_team_construction_failure(self, analyzer, sample_players):
        """Test that roster is invalid if team construction fails"""
        roster = [sample_players['qb1']]

        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            mock_instance.draft_player = Mock(return_value=False)
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster(roster)
            assert result is False


class TestGetTradeCombinations:
    """Test get_trade_combinations method"""

    @pytest.fixture
    def mock_teams(self, sample_players, mock_player_manager):
        """Create mock TradeSimTeam objects"""
        my_roster = [sample_players['qb1'], sample_players['rb1']]
        their_roster = [sample_players['wr1'], sample_players['te1']]

        my_team = Mock(spec=TradeSimTeam)
        my_team.team = my_roster
        my_team.team_score = 45.0
        my_team.name = "My Team"
        my_team.get_scored_players = Mock(return_value=[])

        their_team = Mock(spec=TradeSimTeam)
        their_team.team = their_roster
        their_team.team_score = 37.0
        their_team.name = "Their Team"
        their_team.get_scored_players = Mock(return_value=[])

        return my_team, their_team

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_get_trade_combinations_one_for_one(self, analyzer, mock_teams):
        """Test generating 1-for-1 trade combinations"""
        my_team, their_team = mock_teams

        # Mock validate_roster to return True
        analyzer.validate_roster = Mock(return_value=True)

        # Mock TradeSimTeam constructor
        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            # Create mock teams with improved scores
            mock_my_new = Mock()
            mock_my_new.team_score = 48.0  # Improved from 45.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 40.0  # Improved from 37.0
            mock_their_new.get_scored_players = Mock(return_value=[])

            mock_team_class.side_effect = [mock_my_new, mock_their_new] * 10  # Multiple trades possible

            with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSnapshot') as mock_snapshot:
                mock_snapshot.return_value = Mock()

                results = analyzer.get_trade_combinations(
                    my_team, their_team,
                    one_for_one=True,
                    two_for_two=False,
                    three_for_three=False
                )

                # Should have generated some 1-for-1 trades (2 my players * 2 their players = 4 max)
                assert len(results) > 0

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_get_trade_combinations_two_for_two(self, analyzer, mock_teams):
        """Test generating 2-for-2 trade combinations"""
        my_team, their_team = mock_teams

        # Mock validate_roster to return True
        analyzer.validate_roster = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 48.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 40.0
            mock_their_new.get_scored_players = Mock(return_value=[])

            mock_team_class.side_effect = [mock_my_new, mock_their_new] * 10

            with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSnapshot') as mock_snapshot:
                mock_snapshot.return_value = Mock()

                results = analyzer.get_trade_combinations(
                    my_team, their_team,
                    one_for_one=False,
                    two_for_two=True,
                    three_for_three=False
                )

                # Should have generated some 2-for-2 trades
                assert len(results) > 0

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_get_trade_combinations_no_valid_trades(self, analyzer, mock_teams):
        """Test when no valid trades exist (all violate roster rules)"""
        my_team, their_team = mock_teams

        # Mock validate_roster to always return False
        analyzer.validate_roster = Mock(return_value=False)

        results = analyzer.get_trade_combinations(
            my_team, their_team,
            one_for_one=True,
            two_for_two=False,
            three_for_three=False
        )

        assert len(results) == 0

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_get_trade_combinations_waivers(self, analyzer, mock_teams):
        """Test waiver trades (is_waivers=True skips their roster validation)"""
        my_team, their_team = mock_teams

        # Mock validate_roster: True for my team, False for their team
        analyzer.validate_roster = Mock(side_effect=lambda roster, **kwargs: roster == my_team.team or len(roster) < 5)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 48.0  # Improved from 45.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 30.0  # Doesn't matter for waivers
            mock_their_new.get_scored_players = Mock(return_value=[])

            mock_team_class.side_effect = [mock_my_new, mock_their_new] * 10

            with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSnapshot') as mock_snapshot:
                mock_snapshot.return_value = Mock()

                results = analyzer.get_trade_combinations(
                    my_team, their_team,
                    is_waivers=True,
                    one_for_one=True,
                    two_for_two=False,
                    three_for_three=False
                )

                # Should generate trades even though their roster validation would fail
                assert len(results) > 0

    def test_get_trade_combinations_locked_players_filtered(self, analyzer, sample_players, mock_player_manager):
        """Test that locked players are filtered out"""
        # Create players with locked status
        qb1 = sample_players['qb1']
        qb1.locked = 1  # Locked
        rb1 = sample_players['rb1']
        rb1.locked = 0  # Not locked

        wr1 = sample_players['wr1']
        wr1.locked = 0

        my_team = Mock(spec=TradeSimTeam)
        my_team.team = [qb1, rb1]  # QB locked, RB not locked
        my_team.team_score = 45.0
        my_team.name = "My Team"
        my_team.get_scored_players = Mock(return_value=[])

        their_team = Mock(spec=TradeSimTeam)
        their_team.team = [wr1]
        their_team.team_score = 22.0
        their_team.name = "Their Team"
        their_team.get_scored_players = Mock(return_value=[])

        analyzer.validate_roster = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 48.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 25.0
            mock_their_new.get_scored_players = Mock(return_value=[])

            mock_team_class.side_effect = [mock_my_new, mock_their_new] * 10

            with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSnapshot') as mock_snapshot:
                mock_snapshot.return_value = Mock()

                results = analyzer.get_trade_combinations(
                    my_team, their_team,
                    one_for_one=True,
                    two_for_two=False,
                    three_for_three=False
                )

                # Only RB1 should be tradeable (QB1 is locked)
                # So should generate 1 trade: RB1 for WR1
                assert len(results) == 1

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_get_trade_combinations_only_my_team_improves(self, analyzer, mock_teams):
        """Test that trades where only my team improves are rejected"""
        my_team, their_team = mock_teams

        analyzer.validate_roster = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 48.0  # Improved from 45.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 35.0  # Worse than 37.0
            mock_their_new.get_scored_players = Mock(return_value=[])

            mock_team_class.side_effect = [mock_my_new, mock_their_new] * 10

            results = analyzer.get_trade_combinations(
                my_team, their_team,
                one_for_one=True,
                two_for_two=False,
                three_for_three=False
            )

            # Should reject all trades (their team gets worse)
            assert len(results) == 0

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_get_trade_combinations_only_their_team_improves(self, analyzer, mock_teams):
        """Test that trades where only their team improves are rejected"""
        my_team, their_team = mock_teams

        analyzer.validate_roster = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 43.0  # Worse than 45.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 40.0  # Better than 37.0
            mock_their_new.get_scored_players = Mock(return_value=[])

            mock_team_class.side_effect = [mock_my_new, mock_their_new] * 10

            results = analyzer.get_trade_combinations(
                my_team, their_team,
                one_for_one=True,
                two_for_two=False,
                three_for_three=False
            )

            # Should reject all trades (my team gets worse)
            assert len(results) == 0

    def test_get_trade_combinations_empty_rosters(self, analyzer, mock_player_manager):
        """Test handling of empty rosters"""
        my_team = Mock(spec=TradeSimTeam)
        my_team.team = []
        my_team.team_score = 0.0
        my_team.name = "My Team"

        their_team = Mock(spec=TradeSimTeam)
        their_team.team = []
        their_team.team_score = 0.0
        their_team.name = "Their Team"

        results = analyzer.get_trade_combinations(
            my_team, their_team,
            one_for_one=True,
            two_for_two=False,
            three_for_three=False
        )

        # No trades possible with empty rosters
        assert len(results) == 0

    @patch('league_helper.trade_simulator_mode.trade_analyzer.Constants.MAX_PLAYERS', 15)
    def test_get_trade_combinations_three_for_three(self, analyzer, sample_players, mock_player_manager):
        """Test generating 3-for-3 trade combinations"""
        # Need at least 3 players per team
        my_roster = [sample_players['qb1'], sample_players['rb1'], sample_players['rb2']]
        their_roster = [sample_players['wr1'], sample_players['wr2'], sample_players['te1']]

        my_team = Mock(spec=TradeSimTeam)
        my_team.team = my_roster
        my_team.team_score = 63.0
        my_team.name = "My Team"
        my_team.get_scored_players = Mock(return_value=[])

        their_team = Mock(spec=TradeSimTeam)
        their_team.team = their_roster
        their_team.team_score = 56.0
        their_team.name = "Their Team"
        their_team.get_scored_players = Mock(return_value=[])

        analyzer.validate_roster = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 66.0  # Improved
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 59.0  # Improved
            mock_their_new.get_scored_players = Mock(return_value=[])

            mock_team_class.side_effect = [mock_my_new, mock_their_new] * 10

            with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSnapshot') as mock_snapshot:
                mock_snapshot.return_value = Mock()

                results = analyzer.get_trade_combinations(
                    my_team, their_team,
                    one_for_one=False,
                    two_for_two=False,
                    three_for_three=True
                )

                # Should have generated 3-for-3 trades
                # With 3 players each: C(3,3) * C(3,3) = 1 * 1 = 1 possible trade
                assert len(results) == 1
