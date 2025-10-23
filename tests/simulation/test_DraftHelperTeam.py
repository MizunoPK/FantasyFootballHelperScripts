"""
Unit tests for DraftHelperTeam module

Tests draft recommendations, lineup optimization, and roster management.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from simulation.DraftHelperTeam import DraftHelperTeam
from utils.FantasyPlayer import FantasyPlayer


@pytest.fixture
def mock_player():
    """Create a mock FantasyPlayer"""
    player = Mock(spec=FantasyPlayer)
    player.id = 1
    player.name = "Test Player"
    player.position = "RB"
    player.drafted = 0
    return player


@pytest.fixture
def mock_player2():
    """Create a second mock FantasyPlayer"""
    player = Mock(spec=FantasyPlayer)
    player.id = 2
    player.name = "Test Player 2"
    player.position = "WR"
    player.drafted = 0
    return player


@pytest.fixture
def mock_projected_pm():
    """Create mock PlayerManager for projected data"""
    pm = Mock()
    pm.players = []
    pm.team = Mock()
    pm.team.roster = []
    return pm


@pytest.fixture
def mock_actual_pm():
    """Create mock PlayerManager for actual data"""
    pm = Mock()
    pm.players = []
    pm.team = Mock()
    pm.team.roster = []
    return pm


@pytest.fixture
def mock_config():
    """Create mock ConfigManager"""
    config = Mock()
    config.current_nfl_week = 1
    config.max_positions = {'QB': 2, 'RB': 4, 'WR': 4, 'FLEX': 2, 'TE': 1, 'K': 1, 'DST': 1}
    config.max_players = 15
    return config


@pytest.fixture
def mock_team_data_mgr():
    """Create mock TeamDataManager"""
    return Mock()


@pytest.fixture
def draft_helper_team(mock_projected_pm, mock_actual_pm, mock_config, mock_team_data_mgr):
    """Create DraftHelperTeam instance with mocks"""
    return DraftHelperTeam(
        mock_projected_pm,
        mock_actual_pm,
        mock_config,
        mock_team_data_mgr
    )


class TestDraftHelperTeamInitialization:
    """Test DraftHelperTeam initialization"""

    def test_init_basic(self, mock_projected_pm, mock_actual_pm, mock_config, mock_team_data_mgr):
        """Test basic initialization"""
        team = DraftHelperTeam(
            mock_projected_pm,
            mock_actual_pm,
            mock_config,
            mock_team_data_mgr
        )

        assert team.projected_pm == mock_projected_pm
        assert team.actual_pm == mock_actual_pm
        assert team.config == mock_config
        assert team.team_data_mgr == mock_team_data_mgr
        assert team.roster == []
        assert team.add_to_roster_mgr is None
        assert team.starter_helper_mgr is None

    def test_init_creates_empty_roster(self, draft_helper_team):
        """Test initialization creates empty roster"""
        assert len(draft_helper_team.roster) == 0

    def test_init_stores_managers(self, draft_helper_team, mock_projected_pm, mock_actual_pm):
        """Test initialization stores all manager references"""
        assert draft_helper_team.projected_pm is mock_projected_pm
        assert draft_helper_team.actual_pm is mock_actual_pm


class TestDraftPlayer:
    """Test draft_player method"""

    def test_draft_player_adds_to_roster(self, draft_helper_team, mock_player, mock_projected_pm, mock_actual_pm):
        """Test drafting player adds to roster"""
        # Setup player in both managers
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = mock_player.id
        proj_player.drafted = 0
        mock_projected_pm.players = [proj_player]

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = mock_player.id
        actual_player.drafted = 0
        mock_actual_pm.players = [actual_player]

        draft_helper_team.draft_player(mock_player)

        assert len(draft_helper_team.roster) == 1
        assert draft_helper_team.roster[0] == mock_player

    def test_draft_player_marks_drafted_in_projected_pm(self, draft_helper_team, mock_player, mock_projected_pm, mock_actual_pm):
        """Test drafting marks player as drafted=2 in projected_pm"""
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = mock_player.id
        proj_player.drafted = 0
        mock_projected_pm.players = [proj_player]

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = mock_player.id
        actual_player.drafted = 0
        mock_actual_pm.players = [actual_player]

        draft_helper_team.draft_player(mock_player)

        assert proj_player.drafted == 2

    def test_draft_player_marks_drafted_in_actual_pm(self, draft_helper_team, mock_player, mock_projected_pm, mock_actual_pm):
        """Test drafting marks player as drafted=2 in actual_pm"""
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = mock_player.id
        proj_player.drafted = 0
        mock_projected_pm.players = [proj_player]

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = mock_player.id
        actual_player.drafted = 0
        mock_actual_pm.players = [actual_player]

        draft_helper_team.draft_player(mock_player)

        assert actual_player.drafted == 2

    def test_draft_player_adds_to_team_roster_in_both_managers(self, draft_helper_team, mock_player, mock_projected_pm, mock_actual_pm):
        """Test drafting adds player to team.roster in both PlayerManagers"""
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = mock_player.id
        proj_player.drafted = 0
        mock_projected_pm.players = [proj_player]

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = mock_player.id
        actual_player.drafted = 0
        mock_actual_pm.players = [actual_player]

        draft_helper_team.draft_player(mock_player)

        assert proj_player in mock_projected_pm.team.roster
        assert actual_player in mock_actual_pm.team.roster

    def test_draft_player_multiple_players(self, draft_helper_team, mock_player, mock_player2, mock_projected_pm, mock_actual_pm):
        """Test drafting multiple players accumulates roster"""
        # Setup player 1
        proj_player1 = Mock(spec=FantasyPlayer)
        proj_player1.id = mock_player.id
        proj_player1.drafted = 0

        actual_player1 = Mock(spec=FantasyPlayer)
        actual_player1.id = mock_player.id
        actual_player1.drafted = 0

        # Setup player 2
        proj_player2 = Mock(spec=FantasyPlayer)
        proj_player2.id = mock_player2.id
        proj_player2.drafted = 0

        actual_player2 = Mock(spec=FantasyPlayer)
        actual_player2.id = mock_player2.id
        actual_player2.drafted = 0

        mock_projected_pm.players = [proj_player1, proj_player2]
        mock_actual_pm.players = [actual_player1, actual_player2]

        draft_helper_team.draft_player(mock_player)
        draft_helper_team.draft_player(mock_player2)

        assert len(draft_helper_team.roster) == 2
        assert mock_player in draft_helper_team.roster
        assert mock_player2 in draft_helper_team.roster

    def test_draft_player_does_not_duplicate_in_team_roster(self, draft_helper_team, mock_player, mock_projected_pm, mock_actual_pm):
        """Test drafting same player twice doesn't duplicate in team.roster"""
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = mock_player.id
        proj_player.drafted = 0
        mock_projected_pm.players = [proj_player]

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = mock_player.id
        actual_player.drafted = 0
        mock_actual_pm.players = [actual_player]

        draft_helper_team.draft_player(mock_player)
        draft_helper_team.draft_player(mock_player)

        # Should only appear once in team.roster
        assert mock_projected_pm.team.roster.count(proj_player) == 1
        assert mock_actual_pm.team.roster.count(actual_player) == 1


@patch('simulation.DraftHelperTeam.AddToRosterModeManager')
class TestGetDraftRecommendation:
    """Test get_draft_recommendation method"""

    def test_get_draft_recommendation_returns_top_pick(self, mock_add_to_roster_class, draft_helper_team, mock_player):
        """Test get_draft_recommendation returns top recommendation"""
        # Setup mock recommendation
        mock_rec = Mock()
        mock_rec.player = mock_player
        mock_rec.score = 95.5

        mock_add_to_roster_mgr = Mock()
        mock_add_to_roster_mgr.get_recommendations.return_value = [mock_rec]
        mock_add_to_roster_class.return_value = mock_add_to_roster_mgr

        result = draft_helper_team.get_draft_recommendation()

        assert result == mock_player

    def test_get_draft_recommendation_creates_fresh_manager(self, mock_add_to_roster_class, draft_helper_team, mock_player, mock_config, mock_projected_pm, mock_team_data_mgr):
        """Test get_draft_recommendation creates fresh AddToRosterModeManager"""
        mock_rec = Mock()
        mock_rec.player = mock_player
        mock_rec.score = 95.5

        mock_add_to_roster_mgr = Mock()
        mock_add_to_roster_mgr.get_recommendations.return_value = [mock_rec]
        mock_add_to_roster_class.return_value = mock_add_to_roster_mgr

        draft_helper_team.get_draft_recommendation()

        mock_add_to_roster_class.assert_called_once_with(
            mock_config,
            mock_projected_pm,
            mock_team_data_mgr
        )

    def test_get_draft_recommendation_raises_when_no_recommendations(self, mock_add_to_roster_class, draft_helper_team):
        """Test get_draft_recommendation raises ValueError when no recommendations"""
        mock_add_to_roster_mgr = Mock()
        mock_add_to_roster_mgr.get_recommendations.return_value = []
        mock_add_to_roster_class.return_value = mock_add_to_roster_mgr

        with pytest.raises(ValueError, match="No draft recommendations available"):
            draft_helper_team.get_draft_recommendation()

    def test_get_draft_recommendation_picks_first_not_second(self, mock_add_to_roster_class, draft_helper_team, mock_player, mock_player2):
        """Test get_draft_recommendation always picks first recommendation"""
        mock_rec1 = Mock()
        mock_rec1.player = mock_player
        mock_rec1.score = 95.5

        mock_rec2 = Mock()
        mock_rec2.player = mock_player2
        mock_rec2.score = 94.0

        mock_add_to_roster_mgr = Mock()
        mock_add_to_roster_mgr.get_recommendations.return_value = [mock_rec1, mock_rec2]
        mock_add_to_roster_class.return_value = mock_add_to_roster_mgr

        result = draft_helper_team.get_draft_recommendation()

        assert result == mock_player  # First, not second
        assert result != mock_player2

    def test_get_draft_recommendation_stores_manager(self, mock_add_to_roster_class, draft_helper_team, mock_player):
        """Test get_draft_recommendation stores manager in self.add_to_roster_mgr"""
        mock_rec = Mock()
        mock_rec.player = mock_player
        mock_rec.score = 95.5

        mock_add_to_roster_mgr = Mock()
        mock_add_to_roster_mgr.get_recommendations.return_value = [mock_rec]
        mock_add_to_roster_class.return_value = mock_add_to_roster_mgr

        draft_helper_team.get_draft_recommendation()

        assert draft_helper_team.add_to_roster_mgr == mock_add_to_roster_mgr


@patch('simulation.DraftHelperTeam.StarterHelperModeManager')
class TestSetWeeklyLineup:
    """Test set_weekly_lineup method"""

    def test_set_weekly_lineup_returns_total_points(self, mock_starter_helper_class, draft_helper_team, mock_actual_pm):
        """Test set_weekly_lineup returns total actual points"""
        # Setup mock lineup with 9 starters
        mock_lineup = Mock()

        starters = []
        for i in range(9):
            starter = Mock()
            starter.player = Mock()
            starter.player.id = i
            starters.append(starter)

        mock_lineup.qb = starters[0]
        mock_lineup.rb1 = starters[1]
        mock_lineup.rb2 = starters[2]
        mock_lineup.wr1 = starters[3]
        mock_lineup.wr2 = starters[4]
        mock_lineup.te = starters[5]
        mock_lineup.flex = starters[6]
        mock_lineup.k = starters[7]
        mock_lineup.dst = starters[8]

        mock_starter_helper_mgr = Mock()
        mock_starter_helper_mgr.optimize_lineup.return_value = mock_lineup
        mock_starter_helper_class.return_value = mock_starter_helper_mgr

        # Mock get_weekly_projection to return 10 points for each player
        mock_actual_pm.get_weekly_projection.return_value = (10.0, 0)

        result = draft_helper_team.set_weekly_lineup(week=5)

        assert result == 90.0  # 9 players × 10 points each

    def test_set_weekly_lineup_updates_config_week(self, mock_starter_helper_class, draft_helper_team, mock_config):
        """Test set_weekly_lineup updates config.current_nfl_week"""
        mock_lineup = Mock()
        mock_lineup.qb = None
        mock_lineup.rb1 = None
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        mock_starter_helper_mgr = Mock()
        mock_starter_helper_mgr.optimize_lineup.return_value = mock_lineup
        mock_starter_helper_class.return_value = mock_starter_helper_mgr

        draft_helper_team.set_weekly_lineup(week=7)

        assert mock_config.current_nfl_week == 7

    def test_set_weekly_lineup_creates_fresh_starter_helper(self, mock_starter_helper_class, draft_helper_team, mock_config, mock_projected_pm, mock_team_data_mgr):
        """Test set_weekly_lineup creates fresh StarterHelperModeManager"""
        mock_lineup = Mock()
        mock_lineup.qb = None
        mock_lineup.rb1 = None
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        mock_starter_helper_mgr = Mock()
        mock_starter_helper_mgr.optimize_lineup.return_value = mock_lineup
        mock_starter_helper_class.return_value = mock_starter_helper_mgr

        draft_helper_team.set_weekly_lineup(week=3)

        mock_starter_helper_class.assert_called_once_with(
            mock_config,
            mock_projected_pm,
            mock_team_data_mgr
        )

    def test_set_weekly_lineup_calls_optimize_lineup(self, mock_starter_helper_class, draft_helper_team):
        """Test set_weekly_lineup calls optimize_lineup"""
        mock_lineup = Mock()
        mock_lineup.qb = None
        mock_lineup.rb1 = None
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        mock_starter_helper_mgr = Mock()
        mock_starter_helper_mgr.optimize_lineup.return_value = mock_lineup
        mock_starter_helper_class.return_value = mock_starter_helper_mgr

        draft_helper_team.set_weekly_lineup(week=1)

        mock_starter_helper_mgr.optimize_lineup.assert_called_once()

    def test_set_weekly_lineup_handles_none_starters(self, mock_starter_helper_class, draft_helper_team, mock_actual_pm):
        """Test set_weekly_lineup handles None values in lineup"""
        mock_lineup = Mock()
        mock_lineup.qb = None
        mock_lineup.rb1 = None
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        mock_starter_helper_mgr = Mock()
        mock_starter_helper_mgr.optimize_lineup.return_value = mock_lineup
        mock_starter_helper_class.return_value = mock_starter_helper_mgr

        result = draft_helper_team.set_weekly_lineup(week=1)

        assert result == 0.0  # No starters = 0 points

    def test_set_weekly_lineup_uses_actual_pm_for_scoring(self, mock_starter_helper_class, draft_helper_team, mock_actual_pm):
        """Test set_weekly_lineup uses actual_pm.get_weekly_projection"""
        mock_lineup = Mock()

        starter = Mock()
        starter.player = Mock()
        starter.player.id = 1

        mock_lineup.qb = starter
        mock_lineup.rb1 = None
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        mock_starter_helper_mgr = Mock()
        mock_starter_helper_mgr.optimize_lineup.return_value = mock_lineup
        mock_starter_helper_class.return_value = mock_starter_helper_mgr

        mock_actual_pm.get_weekly_projection.return_value = (25.5, 0)

        result = draft_helper_team.set_weekly_lineup(week=10)

        mock_actual_pm.get_weekly_projection.assert_called_once_with(starter.player, 10)
        assert result == 25.5

    def test_set_weekly_lineup_stores_manager(self, mock_starter_helper_class, draft_helper_team):
        """Test set_weekly_lineup stores manager in self.starter_helper_mgr"""
        mock_lineup = Mock()
        mock_lineup.qb = None
        mock_lineup.rb1 = None
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        mock_starter_helper_mgr = Mock()
        mock_starter_helper_mgr.optimize_lineup.return_value = mock_lineup
        mock_starter_helper_class.return_value = mock_starter_helper_mgr

        draft_helper_team.set_weekly_lineup(week=1)

        assert draft_helper_team.starter_helper_mgr == mock_starter_helper_mgr


class TestMarkPlayerDrafted:
    """Test mark_player_drafted method"""

    def test_mark_player_drafted_sets_drafted_1_in_projected_pm(self, draft_helper_team, mock_projected_pm, mock_actual_pm):
        """Test marking player drafted sets drafted=1 in projected_pm"""
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = 100
        proj_player.drafted = 0
        mock_projected_pm.players = [proj_player]

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = 100
        actual_player.drafted = 0
        mock_actual_pm.players = [actual_player]

        draft_helper_team.mark_player_drafted(100)

        assert proj_player.drafted == 1

    def test_mark_player_drafted_sets_drafted_1_in_actual_pm(self, draft_helper_team, mock_projected_pm, mock_actual_pm):
        """Test marking player drafted sets drafted=1 in actual_pm"""
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = 100
        proj_player.drafted = 0
        mock_projected_pm.players = [proj_player]

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = 100
        actual_player.drafted = 0
        mock_actual_pm.players = [actual_player]

        draft_helper_team.mark_player_drafted(100)

        assert actual_player.drafted == 1

    def test_mark_player_drafted_only_affects_specified_player(self, draft_helper_team, mock_projected_pm, mock_actual_pm):
        """Test marking player drafted only affects the specified player"""
        proj_player1 = Mock(spec=FantasyPlayer)
        proj_player1.id = 100
        proj_player1.drafted = 0

        proj_player2 = Mock(spec=FantasyPlayer)
        proj_player2.id = 200
        proj_player2.drafted = 0

        mock_projected_pm.players = [proj_player1, proj_player2]

        actual_player1 = Mock(spec=FantasyPlayer)
        actual_player1.id = 100
        actual_player1.drafted = 0

        actual_player2 = Mock(spec=FantasyPlayer)
        actual_player2.id = 200
        actual_player2.drafted = 0

        mock_actual_pm.players = [actual_player1, actual_player2]

        draft_helper_team.mark_player_drafted(100)

        assert proj_player1.drafted == 1
        assert proj_player2.drafted == 0
        assert actual_player1.drafted == 1
        assert actual_player2.drafted == 0

    def test_mark_player_drafted_handles_nonexistent_player(self, draft_helper_team, mock_projected_pm, mock_actual_pm):
        """Test marking nonexistent player as drafted doesn't error"""
        mock_projected_pm.players = []
        mock_actual_pm.players = []

        # Should not raise exception
        draft_helper_team.mark_player_drafted(999)


class TestGetRosterSize:
    """Test get_roster_size method"""

    def test_get_roster_size_empty(self, draft_helper_team):
        """Test roster size when empty"""
        assert draft_helper_team.get_roster_size() == 0

    def test_get_roster_size_with_players(self, draft_helper_team, mock_player, mock_player2, mock_projected_pm, mock_actual_pm):
        """Test roster size with players"""
        # Setup players
        proj_player1 = Mock(spec=FantasyPlayer)
        proj_player1.id = mock_player.id
        proj_player1.drafted = 0

        proj_player2 = Mock(spec=FantasyPlayer)
        proj_player2.id = mock_player2.id
        proj_player2.drafted = 0

        mock_projected_pm.players = [proj_player1, proj_player2]

        actual_player1 = Mock(spec=FantasyPlayer)
        actual_player1.id = mock_player.id
        actual_player1.drafted = 0

        actual_player2 = Mock(spec=FantasyPlayer)
        actual_player2.id = mock_player2.id
        actual_player2.drafted = 0

        mock_actual_pm.players = [actual_player1, actual_player2]

        draft_helper_team.draft_player(mock_player)
        draft_helper_team.draft_player(mock_player2)

        assert draft_helper_team.get_roster_size() == 2

    def test_get_roster_size_at_max(self, draft_helper_team, mock_projected_pm, mock_actual_pm):
        """Test roster size at maximum (15 players)"""
        # Add 15 players
        for i in range(15):
            player = Mock(spec=FantasyPlayer)
            player.id = i
            player.name = f"Player {i}"
            player.position = "RB"
            player.drafted = 0

            proj_player = Mock(spec=FantasyPlayer)
            proj_player.id = i
            proj_player.drafted = 0
            mock_projected_pm.players.append(proj_player)

            actual_player = Mock(spec=FantasyPlayer)
            actual_player.id = i
            actual_player.drafted = 0
            mock_actual_pm.players.append(actual_player)

            draft_helper_team.draft_player(player)

        assert draft_helper_team.get_roster_size() == 15


class TestGetRosterPlayers:
    """Test get_roster_players method"""

    def test_get_roster_players_returns_copy(self, draft_helper_team, mock_player, mock_projected_pm, mock_actual_pm):
        """Test get_roster_players returns a copy, not reference"""
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = mock_player.id
        proj_player.drafted = 0
        mock_projected_pm.players = [proj_player]

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = mock_player.id
        actual_player.drafted = 0
        mock_actual_pm.players = [actual_player]

        draft_helper_team.draft_player(mock_player)

        roster = draft_helper_team.get_roster_players()

        assert roster == draft_helper_team.roster
        assert roster is not draft_helper_team.roster

    def test_get_roster_players_empty(self, draft_helper_team):
        """Test get_roster_players when empty"""
        roster = draft_helper_team.get_roster_players()

        assert roster == []

    def test_get_roster_players_contains_all_drafted(self, draft_helper_team, mock_player, mock_player2, mock_projected_pm, mock_actual_pm):
        """Test get_roster_players contains all drafted players"""
        proj_player1 = Mock(spec=FantasyPlayer)
        proj_player1.id = mock_player.id
        proj_player1.drafted = 0

        proj_player2 = Mock(spec=FantasyPlayer)
        proj_player2.id = mock_player2.id
        proj_player2.drafted = 0

        mock_projected_pm.players = [proj_player1, proj_player2]

        actual_player1 = Mock(spec=FantasyPlayer)
        actual_player1.id = mock_player.id
        actual_player1.drafted = 0

        actual_player2 = Mock(spec=FantasyPlayer)
        actual_player2.id = mock_player2.id
        actual_player2.drafted = 0

        mock_actual_pm.players = [actual_player1, actual_player2]

        draft_helper_team.draft_player(mock_player)
        draft_helper_team.draft_player(mock_player2)

        roster = draft_helper_team.get_roster_players()

        assert len(roster) == 2
        assert mock_player in roster
        assert mock_player2 in roster


class TestDraftHelperTeamIntegration:
    """Test realistic integration scenarios"""

    @patch('simulation.DraftHelperTeam.AddToRosterModeManager')
    @patch('simulation.DraftHelperTeam.StarterHelperModeManager')
    def test_full_draft_and_week_cycle(self, mock_starter_helper_class, mock_add_to_roster_class, draft_helper_team, mock_player, mock_projected_pm, mock_actual_pm):
        """Test complete draft and weekly lineup cycle"""
        # Setup draft recommendation
        mock_rec = Mock()
        mock_rec.player = mock_player
        mock_rec.score = 95.5

        mock_add_to_roster_mgr = Mock()
        mock_add_to_roster_mgr.get_recommendations.return_value = [mock_rec]
        mock_add_to_roster_class.return_value = mock_add_to_roster_mgr

        # Setup player in both managers
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = mock_player.id
        proj_player.drafted = 0
        mock_projected_pm.players = [proj_player]

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = mock_player.id
        actual_player.drafted = 0
        mock_actual_pm.players = [actual_player]

        # Draft player
        recommended = draft_helper_team.get_draft_recommendation()
        draft_helper_team.draft_player(recommended)

        assert draft_helper_team.get_roster_size() == 1

        # Setup weekly lineup
        mock_lineup = Mock()
        starter = Mock()
        starter.player = mock_player
        mock_lineup.qb = starter
        mock_lineup.rb1 = None
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        mock_starter_helper_mgr = Mock()
        mock_starter_helper_mgr.optimize_lineup.return_value = mock_lineup
        mock_starter_helper_class.return_value = mock_starter_helper_mgr

        mock_actual_pm.get_weekly_projection.return_value = (20.5, 0)

        # Set weekly lineup
        points = draft_helper_team.set_weekly_lineup(week=1)

        assert points == 20.5

    def test_draft_multiple_mark_opponents(self, draft_helper_team, mock_player, mock_player2, mock_projected_pm, mock_actual_pm):
        """Test drafting own players and marking opponents' drafts"""
        # Setup player 1 (will draft)
        proj_player1 = Mock(spec=FantasyPlayer)
        proj_player1.id = mock_player.id
        proj_player1.drafted = 0

        actual_player1 = Mock(spec=FantasyPlayer)
        actual_player1.id = mock_player.id
        actual_player1.drafted = 0

        # Setup player 2 (will mark as opponent's)
        proj_player2 = Mock(spec=FantasyPlayer)
        proj_player2.id = mock_player2.id
        proj_player2.drafted = 0

        actual_player2 = Mock(spec=FantasyPlayer)
        actual_player2.id = mock_player2.id
        actual_player2.drafted = 0

        mock_projected_pm.players = [proj_player1, proj_player2]
        mock_actual_pm.players = [actual_player1, actual_player2]

        # Draft player 1 for our team
        draft_helper_team.draft_player(mock_player)

        # Mark player 2 as drafted by opponent
        draft_helper_team.mark_player_drafted(mock_player2.id)

        # Verify states
        assert proj_player1.drafted == 2  # Drafted by our team
        assert proj_player2.drafted == 1  # Drafted by opponent
        assert draft_helper_team.get_roster_size() == 1
        assert mock_player in draft_helper_team.get_roster_players()
        assert mock_player2 not in draft_helper_team.get_roster_players()
