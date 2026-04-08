"""
Tests for TradeAnalyzer class

Tests trade analysis, roster validation, and trade combination generation.
Covers position counting, roster validation logic, and trade scenario generation.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
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
    config = Mock()
    config.max_positions = {'QB': 2, 'RB': 4, 'WR': 4, 'FLEX': 2, 'TE': 1, 'K': 1, 'DST': 1}
    config.max_players = 15
    return config


@pytest.fixture
def analyzer(mock_player_manager, mock_config):
    """Create a TradeAnalyzer instance with mocked dependencies"""
    return TradeAnalyzer(mock_player_manager, mock_config)


@pytest.fixture
def sample_players():
    """Create sample FantasyPlayer objects for testing"""
    qb1 = FantasyPlayer(id=1, name="QB1", team="KC", position="QB", fantasy_points=25.0, injury_status="ACTIVE")
    qb1.locked = 0
    rb1 = FantasyPlayer(id=2, name="RB1", team="SF", position="RB", fantasy_points=20.0, injury_status="ACTIVE")
    rb1.locked = 0
    rb2 = FantasyPlayer(id=3, name="RB2", team="BUF", position="RB", fantasy_points=18.0, injury_status="ACTIVE")
    rb2.locked = 0
    wr1 = FantasyPlayer(id=4, name="WR1", team="MIA", position="WR", fantasy_points=22.0, injury_status="ACTIVE")
    wr1.locked = 0
    wr2 = FantasyPlayer(id=5, name="WR2", team="DAL", position="WR", fantasy_points=19.0, injury_status="ACTIVE")
    wr2.locked = 0
    te1 = FantasyPlayer(id=6, name="TE1", team="KC", position="TE", fantasy_points=15.0, injury_status="ACTIVE")
    te1.locked = 0
    k1 = FantasyPlayer(id=7, name="K1", team="BAL", position="K", fantasy_points=10.0, injury_status="ACTIVE")
    k1.locked = 0
    dst1 = FantasyPlayer(id=8, name="DST1", team="PIT", position="DST", fantasy_points=12.0, injury_status="ACTIVE")
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

    def test_validate_valid_roster(self, analyzer, sample_players, mock_config):
        """Test validating a valid roster"""
        mock_config.max_players = 15
        roster = [sample_players['qb1'], sample_players['rb1'], sample_players['wr1']]

        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            mock_instance.draft_player = Mock(return_value=True)
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster(roster)
            assert result is True

    def test_validate_roster_exceeds_max_players(self, analyzer, sample_players, mock_config):
        """Test that roster exceeding MAX_PLAYERS is invalid"""
        mock_config.max_players = 2
        roster = [sample_players['qb1'], sample_players['rb1'], sample_players['wr1']]
        result = analyzer.validate_roster(roster)
        assert result is False

    def test_validate_roster_with_ignore_max_positions(self, analyzer, sample_players, mock_config):
        """Test that ignore_max_positions allows roster over limit for positions but not total"""
        mock_config.max_players = 2
        roster = [sample_players['qb1'], sample_players['rb1'], sample_players['wr1']]
        result = analyzer.validate_roster(roster, ignore_max_positions=True)
        assert result is False

    def test_validate_roster_ignores_position_limits_when_flag_set(self, analyzer, sample_players, mock_config):
        """Test that ignore_max_positions skips position validation"""
        mock_config.max_players = 5
        roster = [sample_players['qb1'], sample_players['rb1']]
        result = analyzer.validate_roster(roster, ignore_max_positions=True)
        assert result is True

    def test_validate_empty_roster(self, analyzer):
        """Test validating an empty roster"""
        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster([])
            assert result is True

    def test_validate_roster_at_max_boundary(self, analyzer, sample_players):
        """Test validating roster at exact MAX_PLAYERS boundary"""
        roster = [sample_players['qb1']] * 15

        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            mock_instance.draft_player = Mock(return_value=True)
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster(roster)
            assert result is True

    def test_validate_roster_with_position_violation(self, analyzer, sample_players):
        """Test that roster with position violations is invalid"""
        roster = [sample_players['qb1'], sample_players['rb1']]

        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            mock_instance.draft_player = Mock(side_effect=[True, False])
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster(roster)
            assert result is False

    def test_validate_roster_team_construction_failure(self, analyzer, sample_players):
        """Test that roster is invalid if team construction fails"""
        roster = [sample_players['qb1']]

        with patch('league_helper.trade_simulator_mode.trade_analyzer.FantasyTeam') as mock_team:
            mock_instance = Mock()
            mock_instance.draft_player = Mock(return_value=False)
            mock_team.return_value = mock_instance

            result = analyzer.validate_roster(roster)
            assert result is False


class TestCountMinPositionViolations:
    """Test count_min_position_violations method"""

    def test_count_violations_roster_meets_all_minimums(self, analyzer, sample_players):
        """Test roster that meets all minimum requirements returns 0 violations"""
        roster = [
            sample_players['qb1'],  # 1 QB (MIN = 1)
            sample_players['rb1'], sample_players['rb2'], sample_players['rb1'],  # 3 RBs (MIN = 3)
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],  # 3 WRs (MIN = 3)
            sample_players['te1'],  # 1 TE (MIN = 1)
            sample_players['k1'],   # 1 K (MIN = 1)
            sample_players['dst1']  # 1 DST (MIN = 1)
        ]
        result = analyzer.count_min_position_violations(roster)
        assert result == 0

    def test_count_violations_one_position_below_minimum(self, analyzer, sample_players):
        """Test roster below minimum for one position returns 1 violation"""
        roster = [
            sample_players['rb1'], sample_players['rb2'], sample_players['rb1'],  # 3 RBs
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],  # 3 WRs
            sample_players['te1'],
            sample_players['k1'],
            sample_players['dst1']
        ]
        result = analyzer.count_min_position_violations(roster)
        assert result == 1

    def test_count_violations_multiple_positions_below_minimum(self, analyzer, sample_players):
        """Test roster below minimum for multiple positions returns correct count"""
        roster = [
            sample_players['rb1'],  # Only 1 RB (MIN = 3)
            sample_players['wr1'],  # Only 1 WR (MIN = 3)
            sample_players['te1'],
            sample_players['k1'],
            sample_players['dst1']
        ]
        result = analyzer.count_min_position_violations(roster)
        assert result == 3

    def test_count_violations_at_exactly_minimum(self, analyzer, sample_players):
        """Test roster at exactly minimum returns 0 violations"""
        roster = [
            sample_players['qb1'],  # 1 QB (exactly MIN)
            sample_players['rb1'], sample_players['rb2'], sample_players['rb1'],  # 3 RBs (exactly MIN)
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],  # 3 WRs (exactly MIN)
            sample_players['te1'],  # 1 TE (exactly MIN)
            sample_players['k1'],   # 1 K (exactly MIN)
            sample_players['dst1']  # 1 DST (exactly MIN)
        ]
        result = analyzer.count_min_position_violations(roster)
        assert result == 0

    def test_count_violations_empty_roster(self, analyzer):
        """Test empty roster returns violations for all positions"""
        roster = []
        result = analyzer.count_min_position_violations(roster)
        assert result == 6


class TestValidateMinPositionsLenient:
    """Test validate_min_positions_lenient method"""

    def test_validate_trade_maintains_minimums(self, analyzer, sample_players):
        """Test trade that maintains minimum requirements returns True"""
        original = [
            sample_players['qb1'],
            sample_players['rb1'], sample_players['rb2'], sample_players['rb1'],
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],
            sample_players['te1'], sample_players['k1'], sample_players['dst1']
        ]
        new = [
            sample_players['qb1'],  # Still have 1 QB
            sample_players['rb1'], sample_players['rb2'], sample_players['rb1'],  # Still have 3 RBs
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],  # Still have 3 WRs
            sample_players['te1'], sample_players['k1'], sample_players['dst1']
        ]
        result = analyzer.validate_min_positions_lenient(original, new)
        assert result is True

    def test_validate_trade_worsens_violations_returns_false(self, analyzer, sample_players):
        """Test trade that worsens violations returns False"""
        original = [
            sample_players['qb1'],  # Has QB
            sample_players['rb1'], sample_players['rb2'],  # 2 RBs (1 violation - short 1 RB)
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],
            sample_players['te1'], sample_players['k1'], sample_players['dst1']
        ]
        new = [
            sample_players['rb1'], sample_players['rb2'],  # Still 2 RBs (1 violation)
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],
            sample_players['te1'], sample_players['k1'], sample_players['dst1']
        ]
        result = analyzer.validate_min_positions_lenient(original, new)
        assert result is False

    def test_validate_trade_keeps_same_violations_returns_true(self, analyzer, sample_players):
        """Test trade that keeps same violations returns True (lenient)"""
        original = [
            sample_players['qb1'],
            sample_players['rb1'], sample_players['rb2'],  # 2 RBs (1 violation - short 1 RB)
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],
            sample_players['te1'], sample_players['k1'], sample_players['dst1']
        ]
        new = [
            sample_players['qb1'],
            sample_players['rb1'], sample_players['rb2'],  # Still 2 RBs (still 1 violation)
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],
            sample_players['te1'], sample_players['k1'], sample_players['dst1']
        ]
        result = analyzer.validate_min_positions_lenient(original, new)
        assert result is True

    def test_validate_trade_improves_violations_returns_true(self, analyzer, sample_players):
        """Test trade that improves violations returns True"""
        original = [
            sample_players['qb1'],
            sample_players['rb1'], sample_players['rb2'],  # 2 RBs (1 violation)
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],
            sample_players['te1'], sample_players['k1'], sample_players['dst1']
        ]
        new = [
            sample_players['qb1'],
            sample_players['rb1'], sample_players['rb2'], sample_players['rb1'],  # 3 RBs (0 violations)
            sample_players['wr1'], sample_players['wr2'], sample_players['wr1'],
            sample_players['te1'], sample_players['k1'], sample_players['dst1']
        ]
        result = analyzer.validate_min_positions_lenient(original, new)
        assert result is True


class TestGetTradeCombinations:
    """Test get_trade_combinations method"""

    @pytest.fixture
    def mock_teams(self, sample_players, mock_player_manager):
        """Create mock TradeSimTeam objects"""
        my_roster = [sample_players['qb1'], sample_players['rb1']]
        their_roster = [sample_players['wr1'], sample_players['te1']]

        my_team = Mock(spec=TradeSimTeam)
        my_team.team = my_roster
        my_team.team_score = 100.0
        my_team.name = "My Team"
        my_team.get_scored_players = Mock(return_value=[])
        my_team.use_weekly_scoring = False

        their_team = Mock(spec=TradeSimTeam)
        their_team.team = their_roster
        their_team.team_score = 100.0
        their_team.name = "Their Team"
        their_team.get_scored_players = Mock(return_value=[])
        their_team.use_weekly_scoring = False

        return my_team, their_team

    def test_get_trade_combinations_one_for_one(self, analyzer, mock_teams):
        """Test generating 1-for-1 trade combinations"""
        my_team, their_team = mock_teams

        analyzer.validate_roster_lenient = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 135.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 135.0
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

                assert len(results) > 0

    def test_get_trade_combinations_two_for_two(self, analyzer, mock_teams):
        """Test generating 2-for-2 trade combinations"""
        my_team, their_team = mock_teams

        analyzer.validate_roster_lenient = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 135.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 135.0
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

                assert len(results) > 0

    def test_get_trade_combinations_no_valid_trades(self, analyzer, mock_teams):
        """Test when no valid trades exist (all violate roster rules)"""
        my_team, their_team = mock_teams

        analyzer.validate_roster_lenient = Mock(return_value=False)

        results = analyzer.get_trade_combinations(
            my_team, their_team,
            one_for_one=True,
            two_for_two=False,
            three_for_three=False
        )

        assert len(results) == 0

    def test_get_trade_combinations_waivers(self, analyzer, mock_teams):
        """Test waiver trades (is_waivers=True skips their roster validation)"""
        my_team, their_team = mock_teams

        analyzer.validate_roster_lenient = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 106.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 30.0
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

                assert len(results) > 0

    def test_get_trade_combinations_locked_players_filtered(self, analyzer, sample_players, mock_player_manager):
        """Test that locked players are filtered out"""
        qb1 = sample_players['qb1']
        qb1.locked = 1
        rb1 = sample_players['rb1']
        rb1.locked = 0

        wr1 = sample_players['wr1']
        wr1.locked = 0

        my_team = Mock(spec=TradeSimTeam)
        my_team.team = [qb1, rb1]
        my_team.team_score = 100.0
        my_team.name = "My Team"
        my_team.get_scored_players = Mock(return_value=[])
        my_team.use_weekly_scoring = False

        their_team = Mock(spec=TradeSimTeam)
        their_team.team = [wr1]
        their_team.team_score = 100.0
        their_team.name = "Their Team"
        their_team.get_scored_players = Mock(return_value=[])
        their_team.use_weekly_scoring = False

        analyzer.validate_roster_lenient = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 135.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 135.0
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

                assert len(results) == 1

    def test_get_trade_combinations_only_my_team_improves(self, analyzer, mock_teams):
        """Test that trades where only my team improves are rejected"""
        my_team, their_team = mock_teams

        analyzer.validate_roster_lenient = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 135.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 95.0
            mock_their_new.get_scored_players = Mock(return_value=[])

            mock_team_class.side_effect = [mock_my_new, mock_their_new] * 10

            results = analyzer.get_trade_combinations(
                my_team, their_team,
                one_for_one=True,
                two_for_two=False,
                three_for_three=False
            )

            assert len(results) == 0

    def test_get_trade_combinations_only_their_team_improves(self, analyzer, mock_teams):
        """Test that trades where only their team improves are rejected"""
        my_team, their_team = mock_teams

        analyzer.validate_roster_lenient = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 95.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 135.0
            mock_their_new.get_scored_players = Mock(return_value=[])

            mock_team_class.side_effect = [mock_my_new, mock_their_new] * 10

            results = analyzer.get_trade_combinations(
                my_team, their_team,
                one_for_one=True,
                two_for_two=False,
                three_for_three=False
            )

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

        assert len(results) == 0

    def test_get_trade_combinations_three_for_three(self, analyzer, sample_players, mock_player_manager):
        """Test generating 3-for-3 trade combinations"""
        my_roster = [sample_players['qb1'], sample_players['rb1'], sample_players['rb2']]
        their_roster = [sample_players['wr1'], sample_players['wr2'], sample_players['te1']]

        my_team = Mock(spec=TradeSimTeam)
        my_team.team = my_roster
        my_team.team_score = 100.0
        my_team.name = "My Team"
        my_team.get_scored_players = Mock(return_value=[])
        my_team.use_weekly_scoring = False

        their_team = Mock(spec=TradeSimTeam)
        their_team.team = their_roster
        their_team.team_score = 100.0
        their_team.name = "Their Team"
        their_team.get_scored_players = Mock(return_value=[])
        their_team.use_weekly_scoring = False

        analyzer.validate_roster_lenient = Mock(return_value=True)

        with patch('league_helper.trade_simulator_mode.trade_analyzer.TradeSimTeam') as mock_team_class:
            mock_my_new = Mock()
            mock_my_new.team_score = 135.0
            mock_my_new.get_scored_players = Mock(return_value=[])

            mock_their_new = Mock()
            mock_their_new.team_score = 135.0
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

                assert len(results) == 1


