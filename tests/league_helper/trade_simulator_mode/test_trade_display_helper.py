"""
Unit Tests for TradeDisplayHelper

Tests the TradeDisplayHelper class which handles formatting and display of
trade-related information including rosters, combined team views, and trade
impact analysis.

Author: Claude Code
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock
from typing import List

# Add league_helper to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "league_helper"))
from trade_simulator_mode.trade_display_helper import TradeDisplayHelper
from trade_simulator_mode.TradeSnapshot import TradeSnapshot
from trade_simulator_mode.TradeSimTeam import TradeSimTeam

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer


class TestTradeDisplayHelperInitialization:
    """Test TradeDisplayHelper class structure and initialization"""

    def test_class_exists(self):
        """Test that TradeDisplayHelper class exists and can be instantiated"""
        helper = TradeDisplayHelper()
        assert helper is not None

    def test_all_methods_are_static(self):
        """Test that all display methods are static methods"""
        assert callable(TradeDisplayHelper.display_numbered_roster)
        assert callable(TradeDisplayHelper.display_combined_roster)
        assert callable(TradeDisplayHelper.display_trade_result)


class TestDisplayNumberedRoster:
    """Test display_numbered_roster method"""

    def test_display_empty_roster(self, capsys):
        """Test displaying an empty roster"""
        TradeDisplayHelper.display_numbered_roster([], "EMPTY ROSTER")

        captured = capsys.readouterr()
        assert "EMPTY ROSTER" in captured.out
        assert "=" * 25 in captured.out
        # Should only have title and separators, no player listings
        lines = [line for line in captured.out.split('\n') if line.strip() and '=' not in line]
        assert len(lines) == 1  # Only title

    def test_display_single_player(self, capsys):
        """Test displaying roster with single player"""
        player = FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB")
        TradeDisplayHelper.display_numbered_roster([player], "MY ROSTER")

        captured = capsys.readouterr()
        assert "MY ROSTER" in captured.out
        assert "1." in captured.out
        assert "Patrick Mahomes" in captured.out

    def test_display_multiple_players(self, capsys):
        """Test displaying roster with multiple players"""
        players = [
            FantasyPlayer(id=1, name="Player1", team="KC", position="QB"),
            FantasyPlayer(id=2, name="Player2", team="SF", position="RB"),
            FantasyPlayer(id=3, name="Player3", team="MIA", position="WR"),
        ]
        TradeDisplayHelper.display_numbered_roster(players, "TEST ROSTER")

        captured = capsys.readouterr()
        assert "TEST ROSTER" in captured.out
        assert "1. " in captured.out
        assert "2. " in captured.out
        assert "3. " in captured.out
        assert "Player1" in captured.out
        assert "Player2" in captured.out
        assert "Player3" in captured.out

    def test_display_roster_numbering_starts_at_one(self, capsys):
        """Test that roster numbering starts at 1 not 0"""
        players = [FantasyPlayer(id=1, name="Test", team="KC", position="QB")]
        TradeDisplayHelper.display_numbered_roster(players, "NUMBERING TEST")

        captured = capsys.readouterr()
        # Check that numbering starts with "1. " (note the space after the period)
        assert "1. Test" in captured.out
        # Make sure there's no "0. " numbering (with space)
        assert "\n0. " not in captured.out

    def test_display_roster_with_long_title(self, capsys):
        """Test displaying roster with very long title"""
        long_title = "A" * 100
        players = [FantasyPlayer(id=1, name="Test", team="KC", position="QB")]
        TradeDisplayHelper.display_numbered_roster(players, long_title)

        captured = capsys.readouterr()
        assert long_title in captured.out


class TestDisplayCombinedRoster:
    """Test display_combined_roster method"""

    def test_display_both_empty_rosters(self, capsys):
        """Test displaying when both rosters are empty"""
        boundary, my_order, their_order = TradeDisplayHelper.display_combined_roster(
            [], [], "Opponent"
        )

        captured = capsys.readouterr()
        assert "COMBINED ROSTER FOR TRADE" in captured.out
        assert "MY TEAM" in captured.out
        assert "OPPONENT" in captured.out
        assert "(No players)" in captured.out
        assert boundary == 1
        assert len(my_order) == 0
        assert len(their_order) == 0

    def test_display_only_my_roster_has_players(self, capsys):
        """Test when only my roster has players"""
        my_roster = [
            FantasyPlayer(id=1, name="MyQB", team="KC", position="QB", fantasy_points=25.0),
        ]
        boundary, my_order, their_order = TradeDisplayHelper.display_combined_roster(
            my_roster, [], "Empty Team"
        )

        captured = capsys.readouterr()
        assert "MY TEAM" in captured.out
        assert "EMPTY TEAM" in captured.out
        assert "MyQB" in captured.out
        assert boundary == 2  # Boundary is after my 1 player
        assert len(my_order) == 1
        assert len(their_order) == 0

    def test_display_only_their_roster_has_players(self, capsys):
        """Test when only opponent roster has players"""
        their_roster = [
            FantasyPlayer(id=1, name="TheirQB", team="BUF", position="QB", fantasy_points=24.0),
        ]
        boundary, my_order, their_order = TradeDisplayHelper.display_combined_roster(
            [], their_roster, "Opponent"
        )

        captured = capsys.readouterr()
        assert "TheirQB" in captured.out
        assert boundary == 1  # Boundary is at start (no my players)
        assert len(my_order) == 0
        assert len(their_order) == 1

    def test_display_combined_rosters_with_same_positions(self, capsys):
        """Test combined display when both teams have same positions"""
        my_roster = [
            FantasyPlayer(id=1, name="MyQB", team="KC", position="QB", fantasy_points=25.0),
            FantasyPlayer(id=2, name="MyRB", team="SF", position="RB", fantasy_points=20.0),
        ]
        their_roster = [
            FantasyPlayer(id=3, name="TheirQB", team="BUF", position="QB", fantasy_points=24.0),
            FantasyPlayer(id=4, name="TheirRB", team="DAL", position="RB", fantasy_points=19.0),
        ]
        boundary, my_order, their_order = TradeDisplayHelper.display_combined_roster(
            my_roster, their_roster, "Opponent"
        )

        captured = capsys.readouterr()
        assert "QB:" in captured.out
        assert "RB:" in captured.out
        assert "MyQB" in captured.out
        assert "MyRB" in captured.out
        assert "TheirQB" in captured.out
        assert "TheirRB" in captured.out
        assert boundary == 3  # After 2 my players
        assert len(my_order) == 2
        assert len(their_order) == 2

    def test_display_combined_rosters_sorted_by_score(self, capsys):
        """Test that players within position are sorted by score descending"""
        # Create players with score attribute (used by TradeSimulator for sorting)
        low_rb = FantasyPlayer(id=1, name="LowRB", team="JAX", position="RB", fantasy_points=10.0)
        low_rb.score = 10.0
        high_rb = FantasyPlayer(id=2, name="HighRB", team="SF", position="RB", fantasy_points=25.0)
        high_rb.score = 25.0
        mid_rb = FantasyPlayer(id=3, name="MidRB", team="DAL", position="RB", fantasy_points=18.0)
        mid_rb.score = 18.0

        my_roster = [low_rb, high_rb, mid_rb]
        boundary, my_order, their_order = TradeDisplayHelper.display_combined_roster(
            my_roster, [], "Empty"
        )

        # Check display order is by score (highest first)
        assert my_order[0].name == "HighRB"
        assert my_order[1].name == "MidRB"
        assert my_order[2].name == "LowRB"

    def test_display_combined_rosters_position_order(self, capsys):
        """Test that positions are displayed in correct order: QB, RB, WR, TE, K, DST"""
        my_roster = [
            FantasyPlayer(id=1, name="DST", team="SF", position="DST", fantasy_points=12.0),
            FantasyPlayer(id=2, name="QB", team="KC", position="QB", fantasy_points=25.0),
            FantasyPlayer(id=3, name="WR", team="MIA", position="WR", fantasy_points=20.0),
        ]
        boundary, my_order, their_order = TradeDisplayHelper.display_combined_roster(
            my_roster, [], "Test"
        )

        captured = capsys.readouterr()
        # Check that positions appear in order in output
        qb_pos = captured.out.index("QB:")
        rb_pos = captured.out.index("RB:")
        wr_pos = captured.out.index("WR:")
        te_pos = captured.out.index("TE:")
        k_pos = captured.out.index("K:")
        dst_pos = captured.out.index("DST:")

        assert qb_pos < rb_pos < wr_pos < te_pos < k_pos < dst_pos

    def test_display_combined_boundary_calculation(self):
        """Test that boundary is calculated correctly"""
        my_roster = [
            FantasyPlayer(id=1, name="QB1", team="KC", position="QB", fantasy_points=25.0),
            FantasyPlayer(id=2, name="RB1", team="SF", position="RB", fantasy_points=20.0),
            FantasyPlayer(id=3, name="RB2", team="DAL", position="RB", fantasy_points=18.0),
        ]
        their_roster = [
            FantasyPlayer(id=4, name="QB2", team="BUF", position="QB", fantasy_points=24.0),
        ]
        boundary, my_order, their_order = TradeDisplayHelper.display_combined_roster(
            my_roster, their_roster, "Opponent"
        )

        # Boundary should be 4 (after 3 my players, their numbering starts at 4)
        assert boundary == 4
        assert len(my_order) == 3
        assert len(their_order) == 1

    def test_display_combined_uppercase_team_name(self, capsys):
        """Test that opponent team name is displayed in uppercase"""
        TradeDisplayHelper.display_combined_roster([], [], "lowercase team")

        captured = capsys.readouterr()
        assert "LOWERCASE TEAM" in captured.out
        assert "lowercase team" not in captured.out


class TestDisplayTradeResult:
    """Test display_trade_result method"""

    @pytest.fixture
    def mock_trade(self):
        """Create a mock TradeSnapshot for testing"""
        # Create mock teams
        my_team = Mock(spec=TradeSimTeam)
        my_team.name = "My Team"
        my_team.team_score = 150.0

        their_team = Mock(spec=TradeSimTeam)
        their_team.name = "Their Team"
        their_team.team_score = 140.0

        # Create mock players
        my_give = [Mock(spec=Mock)]
        my_give[0].__str__ = Mock(return_value="Player1 (QB) - KC - 25.0 pts")

        my_receive = [Mock(spec=Mock)]
        my_receive[0].__str__ = Mock(return_value="Player2 (RB) - SF - 22.0 pts")

        # Create mock trade
        trade = Mock(spec=TradeSnapshot)
        trade.my_new_team = my_team
        trade.their_new_team = their_team
        trade.my_original_players = my_give
        trade.my_new_players = my_receive
        # Add new unequal trade fields (default to None/empty for basic tests)
        trade.waiver_recommendations = None
        trade.their_waiver_recommendations = None
        trade.my_dropped_players = None
        trade.their_dropped_players = None

        return trade

    def test_display_trade_positive_improvement_for_both(self, mock_trade, capsys):
        """Test displaying trade where both teams improve"""
        TradeDisplayHelper.display_trade_result(mock_trade, 145.0, 135.0)

        captured = capsys.readouterr()
        assert "MANUAL TRADE VISUALIZER - Trade Impact Analysis" in captured.out
        assert "Trade with Their Team" in captured.out
        assert "My improvement: +5.00 pts" in captured.out
        assert "Their improvement: +5.00 pts" in captured.out
        assert "New score: 150.00" in captured.out
        assert "New score: 140.00" in captured.out

    def test_display_trade_negative_improvement(self, mock_trade, capsys):
        """Test displaying trade with negative improvement (losing trade)"""
        TradeDisplayHelper.display_trade_result(mock_trade, 155.0, 145.0)

        captured = capsys.readouterr()
        assert "My improvement: -5.00 pts" in captured.out
        assert "Their improvement: -5.00 pts" in captured.out

    def test_display_trade_zero_improvement(self, mock_trade, capsys):
        """Test displaying trade with zero improvement (even trade)"""
        TradeDisplayHelper.display_trade_result(mock_trade, 150.0, 140.0)

        captured = capsys.readouterr()
        assert "My improvement: +0.00 pts" in captured.out
        assert "Their improvement: +0.00 pts" in captured.out

    def test_display_trade_shows_players_given(self, mock_trade, capsys):
        """Test that trade display shows players given"""
        TradeDisplayHelper.display_trade_result(mock_trade, 145.0, 135.0)

        captured = capsys.readouterr()
        assert "I give:" in captured.out
        assert "Player1 (QB) - KC - 25.0 pts" in captured.out

    def test_display_trade_shows_players_received(self, mock_trade, capsys):
        """Test that trade display shows players received"""
        TradeDisplayHelper.display_trade_result(mock_trade, 145.0, 135.0)

        captured = capsys.readouterr()
        assert "I receive:" in captured.out
        assert "Player2 (RB) - SF - 22.0 pts" in captured.out

    def test_display_trade_multiple_players(self, capsys):
        """Test displaying trade with multiple players on each side"""
        # Create trade with multiple players
        my_team = Mock(spec=TradeSimTeam)
        my_team.name = "My Team"
        my_team.team_score = 150.0

        their_team = Mock(spec=TradeSimTeam)
        their_team.name = "Their Team"
        their_team.team_score = 140.0

        # Multiple players
        give1 = Mock()
        give1.__str__ = Mock(return_value="Give1 (QB) - KC")
        give2 = Mock()
        give2.__str__ = Mock(return_value="Give2 (RB) - SF")

        receive1 = Mock()
        receive1.__str__ = Mock(return_value="Receive1 (WR) - MIA")
        receive2 = Mock()
        receive2.__str__ = Mock(return_value="Receive2 (TE) - KC")

        trade = Mock(spec=TradeSnapshot)
        trade.my_new_team = my_team
        trade.their_new_team = their_team
        trade.my_original_players = [give1, give2]
        trade.my_new_players = [receive1, receive2]
        # Add new unequal trade fields (default to None/empty for basic tests)
        trade.waiver_recommendations = None
        trade.their_waiver_recommendations = None
        trade.my_dropped_players = None
        trade.their_dropped_players = None

        TradeDisplayHelper.display_trade_result(trade, 145.0, 135.0)

        captured = capsys.readouterr()
        assert "Give1" in captured.out
        assert "Give2" in captured.out
        assert "Receive1" in captured.out
        assert "Receive2" in captured.out


class TestTradeDisplayHelperEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_display_roster_with_special_characters_in_name(self, capsys):
        """Test displaying player with special characters in name"""
        player = FantasyPlayer(id=1, name="D'Andre Swift", team="PHI", position="RB")
        TradeDisplayHelper.display_numbered_roster([player], "SPECIAL CHARS")

        captured = capsys.readouterr()
        assert "D'Andre Swift" in captured.out

    def test_display_roster_with_very_long_player_name(self, capsys):
        """Test displaying player with very long name"""
        long_name = "A" * 100
        player = FantasyPlayer(id=1, name=long_name, team="KC", position="QB")
        TradeDisplayHelper.display_numbered_roster([player], "LONG NAME")

        captured = capsys.readouterr()
        assert long_name in captured.out

    def test_display_combined_roster_returns_correct_types(self):
        """Test that display_combined_roster returns correct types"""
        my_roster = [FantasyPlayer(id=1, name="Test", team="KC", position="QB", fantasy_points=25.0)]
        their_roster = []

        result = TradeDisplayHelper.display_combined_roster(my_roster, their_roster, "Test")

        assert isinstance(result, tuple)
        assert len(result) == 3
        assert isinstance(result[0], int)  # boundary
        assert isinstance(result[1], list)  # my_order
        assert isinstance(result[2], list)  # their_order

    def test_display_large_rosters(self, capsys):
        """Test displaying very large rosters (15 players each)"""
        my_roster = [
            FantasyPlayer(id=i, name=f"MyPlayer{i}", team="KC", position="RB", fantasy_points=20.0-i)
            for i in range(15)
        ]
        their_roster = [
            FantasyPlayer(id=i+100, name=f"TheirPlayer{i}", team="BUF", position="RB", fantasy_points=19.0-i)
            for i in range(15)
        ]

        boundary, my_order, their_order = TradeDisplayHelper.display_combined_roster(
            my_roster, their_roster, "Large Team"
        )

        assert len(my_order) == 15
        assert len(their_order) == 15
        assert boundary == 16  # After 15 my players


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
