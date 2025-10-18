"""
Tests for TradeInputParser class

Tests parsing and validation of user input for trade selections.
Covers all static methods for input parsing, player extraction, and team splitting.

Author: Kai Mizuno
"""

import pytest
import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from league_helper.trade_simulator_mode.trade_input_parser import TradeInputParser


class TestTradeInputParserInitialization:
    """Test TradeInputParser class structure and initialization"""

    def test_class_exists(self):
        """Test that TradeInputParser class exists"""
        assert TradeInputParser is not None
        assert hasattr(TradeInputParser, '__name__')
        assert TradeInputParser.__name__ == 'TradeInputParser'

    def test_all_methods_are_static(self):
        """Test that all methods are static"""
        assert isinstance(TradeInputParser.__dict__['parse_player_selection'], staticmethod)
        assert isinstance(TradeInputParser.__dict__['get_players_by_indices'], staticmethod)
        assert isinstance(TradeInputParser.__dict__['split_players_by_team'], staticmethod)
        assert isinstance(TradeInputParser.__dict__['parse_unified_player_selection'], staticmethod)


class TestParsePlayerSelection:
    """Test parse_player_selection method"""

    def test_parse_single_number(self):
        """Test parsing a single valid number"""
        result = TradeInputParser.parse_player_selection("3", 10)
        assert result == [3]

    def test_parse_multiple_numbers(self):
        """Test parsing multiple valid numbers"""
        result = TradeInputParser.parse_player_selection("1,2,3", 10)
        assert result == [1, 2, 3]

    def test_parse_with_spaces(self):
        """Test parsing with spaces around commas and numbers"""
        result = TradeInputParser.parse_player_selection(" 1 , 2 , 3 ", 10)
        assert result == [1, 2, 3]

    def test_parse_exit_lowercase(self):
        """Test that 'exit' returns None"""
        result = TradeInputParser.parse_player_selection("exit", 10)
        assert result is None

    def test_parse_exit_uppercase(self):
        """Test that 'EXIT' returns None"""
        result = TradeInputParser.parse_player_selection("EXIT", 10)
        assert result is None

    def test_parse_empty_input(self):
        """Test that empty input returns None"""
        result = TradeInputParser.parse_player_selection("", 10)
        assert result is None

    def test_parse_whitespace_only(self):
        """Test that whitespace-only input returns None"""
        result = TradeInputParser.parse_player_selection("   ", 10)
        assert result is None

    def test_parse_invalid_characters(self):
        """Test that invalid characters return None"""
        result = TradeInputParser.parse_player_selection("1,abc,3", 10)
        assert result is None

    def test_parse_out_of_range_too_low(self):
        """Test that numbers below 1 return None"""
        result = TradeInputParser.parse_player_selection("0,2,3", 10)
        assert result is None

    def test_parse_out_of_range_too_high(self):
        """Test that numbers above max_index return None"""
        result = TradeInputParser.parse_player_selection("1,2,11", 10)
        assert result is None

    def test_parse_duplicate_numbers(self):
        """Test that duplicate numbers return None"""
        result = TradeInputParser.parse_player_selection("1,2,2,3", 10)
        assert result is None

    def test_parse_max_boundary(self):
        """Test parsing number at max boundary"""
        result = TradeInputParser.parse_player_selection("10", 10)
        assert result == [10]

    def test_parse_min_boundary(self):
        """Test parsing number at min boundary"""
        result = TradeInputParser.parse_player_selection("1", 10)
        assert result == [1]


class TestGetPlayersByIndices:
    """Test get_players_by_indices method"""

    def test_get_single_player(self):
        """Test extracting a single player"""
        player1 = FantasyPlayer(id=1, name="Player1", team="KC", position="QB", fantasy_points=20.0)
        player2 = FantasyPlayer(id=2, name="Player2", team="SF", position="RB", fantasy_points=15.0)
        roster = [player1, player2]

        result = TradeInputParser.get_players_by_indices(roster, [1])
        assert len(result) == 1
        assert result[0].name == "Player1"

    def test_get_multiple_players(self):
        """Test extracting multiple players"""
        player1 = FantasyPlayer(id=1, name="Player1", team="KC", position="QB", fantasy_points=20.0)
        player2 = FantasyPlayer(id=2, name="Player2", team="SF", position="RB", fantasy_points=15.0)
        player3 = FantasyPlayer(id=3, name="Player3", team="BUF", position="WR", fantasy_points=12.0)
        roster = [player1, player2, player3]

        result = TradeInputParser.get_players_by_indices(roster, [1, 3])
        assert len(result) == 2
        assert result[0].name == "Player1"
        assert result[1].name == "Player3"

    def test_get_players_preserves_order(self):
        """Test that player extraction preserves input order"""
        player1 = FantasyPlayer(id=1, name="Player1", team="KC", position="QB", fantasy_points=20.0)
        player2 = FantasyPlayer(id=2, name="Player2", team="SF", position="RB", fantasy_points=15.0)
        player3 = FantasyPlayer(id=3, name="Player3", team="BUF", position="WR", fantasy_points=12.0)
        roster = [player1, player2, player3]

        result = TradeInputParser.get_players_by_indices(roster, [3, 1, 2])
        assert len(result) == 3
        assert result[0].name == "Player3"
        assert result[1].name == "Player1"
        assert result[2].name == "Player2"

    def test_get_players_empty_indices(self):
        """Test extracting with empty indices list"""
        player1 = FantasyPlayer(id=1, name="Player1", team="KC", position="QB", fantasy_points=20.0)
        roster = [player1]

        result = TradeInputParser.get_players_by_indices(roster, [])
        assert len(result) == 0


class TestSplitPlayersByTeam:
    """Test split_players_by_team method"""

    def test_split_only_my_players(self):
        """Test splitting with only my players selected"""
        unified_indices = [1, 2, 3]
        roster_boundary = 14

        my_indices, their_indices = TradeInputParser.split_players_by_team(unified_indices, roster_boundary)
        assert my_indices == [1, 2, 3]
        assert their_indices == []

    def test_split_only_their_players(self):
        """Test splitting with only their players selected"""
        unified_indices = [14, 15, 16]
        roster_boundary = 14

        my_indices, their_indices = TradeInputParser.split_players_by_team(unified_indices, roster_boundary)
        assert my_indices == []
        assert their_indices == [1, 2, 3]  # Adjusted to be 1-based relative to their roster

    def test_split_mixed_players(self):
        """Test splitting with players from both teams"""
        unified_indices = [2, 6, 14, 21]
        roster_boundary = 14

        my_indices, their_indices = TradeInputParser.split_players_by_team(unified_indices, roster_boundary)
        assert my_indices == [2, 6]
        assert their_indices == [1, 8]  # 14->1, 21->8 (adjusted to be relative)

    def test_split_boundary_player(self):
        """Test splitting with player exactly at boundary"""
        unified_indices = [13, 14]
        roster_boundary = 14

        my_indices, their_indices = TradeInputParser.split_players_by_team(unified_indices, roster_boundary)
        assert my_indices == [13]
        assert their_indices == [1]  # 14 is first player in their roster

    def test_split_correct_adjustment_of_their_indices(self):
        """Test that their indices are correctly adjusted to 1-based"""
        unified_indices = [20, 25, 30]
        roster_boundary = 15

        my_indices, their_indices = TradeInputParser.split_players_by_team(unified_indices, roster_boundary)
        assert my_indices == []
        assert their_indices == [6, 11, 16]  # 20->6, 25->11, 30->16


class TestParseUnifiedPlayerSelection:
    """Test parse_unified_player_selection method"""

    def test_parse_valid_balanced_trade(self):
        """Test parsing valid trade with equal players from each team"""
        result = TradeInputParser.parse_unified_player_selection("2,6,18,21", 30, 14)
        assert result is not None
        my_indices, their_indices = result
        assert my_indices == [2, 6]
        assert their_indices == [5, 8]  # 18->5, 21->8

    def test_parse_invalid_all_from_my_team(self):
        """Test that selecting only from my team returns None"""
        result = TradeInputParser.parse_unified_player_selection("1,2,3,4", 30, 14)
        assert result is None

    def test_parse_invalid_all_from_their_team(self):
        """Test that selecting only from their team returns None"""
        result = TradeInputParser.parse_unified_player_selection("14,15,16,17", 30, 14)
        assert result is None

    def test_parse_invalid_unequal_numbers(self):
        """Test that unequal numbers from each team returns None"""
        result = TradeInputParser.parse_unified_player_selection("1,2,14", 30, 14)
        assert result is None

    def test_parse_invalid_input_string(self):
        """Test that invalid input string returns None"""
        result = TradeInputParser.parse_unified_player_selection("1,abc,14,15", 30, 14)
        assert result is None

    def test_parse_exit(self):
        """Test that 'exit' returns None"""
        result = TradeInputParser.parse_unified_player_selection("exit", 30, 14)
        assert result is None

    def test_parse_valid_multiple_players_per_team(self):
        """Test valid trade with 3 players from each team"""
        result = TradeInputParser.parse_unified_player_selection("1,2,3,14,15,16", 30, 14)
        assert result is not None
        my_indices, their_indices = result
        assert my_indices == [1, 2, 3]
        assert their_indices == [1, 2, 3]

    def test_parse_valid_single_player_each(self):
        """Test valid trade with 1 player from each team"""
        result = TradeInputParser.parse_unified_player_selection("5,20", 30, 14)
        assert result is not None
        my_indices, their_indices = result
        assert my_indices == [5]
        assert their_indices == [7]  # 20->7

    def test_parse_boundary_case(self):
        """Test parsing with player at exact boundary"""
        result = TradeInputParser.parse_unified_player_selection("13,14", 30, 14)
        assert result is not None
        my_indices, their_indices = result
        assert my_indices == [13]
        assert their_indices == [1]  # 14 is first player in their roster

    def test_parse_out_of_range(self):
        """Test that out of range indices return None"""
        result = TradeInputParser.parse_unified_player_selection("1,2,14,99", 30, 14)
        assert result is None

    def test_parse_duplicates(self):
        """Test that duplicate indices return None"""
        result = TradeInputParser.parse_unified_player_selection("1,1,14,15", 30, 14)
        assert result is None
