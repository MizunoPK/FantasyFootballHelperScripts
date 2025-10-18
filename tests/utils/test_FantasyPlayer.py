"""
Tests for FantasyPlayer class.

Comprehensive tests for all FantasyPlayer functionality including initialization,
factory methods, properties, and helper functions.

Author: Kai Mizuno
"""

import pytest
from utils.FantasyPlayer import FantasyPlayer, safe_int_conversion, safe_float_conversion


class TestFantasyPlayerLockedIndicator:
    """Test suite for FantasyPlayer [LOCKED] indicator in __str__() method."""

    def test_str_shows_locked_indicator_when_locked_is_one(self):
        """Test that [LOCKED] appears at end of string when locked=1."""
        # Arrange
        player = FantasyPlayer(
            id=1,
            name="Test Player",
            team="KC",
            position="QB",
            bye_week=7,
            drafted=0,
            locked=1,  # Player is locked
            score=85.5,
            fantasy_points=250.0
        )

        # Act
        player_str = str(player)

        # Assert
        assert " [LOCKED]" in player_str, "Expected [LOCKED] indicator in player string"
        assert player_str.endswith("[LOCKED]"), "Expected [LOCKED] to be at the end of string"

    def test_str_no_locked_indicator_when_locked_is_zero(self):
        """Test that [LOCKED] does NOT appear when locked=0."""
        # Arrange
        player = FantasyPlayer(
            id=2,
            name="Available Player",
            team="KC",
            position="RB",
            bye_week=7,
            drafted=0,
            locked=0,  # Player is NOT locked
            score=75.0,
            fantasy_points=200.0
        )

        # Act
        player_str = str(player)

        # Assert
        assert " [LOCKED]" not in player_str, "Did not expect [LOCKED] indicator when locked=0"
        assert not player_str.endswith("[LOCKED]"), "[LOCKED] should not be at end when locked=0"

    def test_str_locked_indicator_with_drafted_status(self):
        """Test that [LOCKED] works correctly with different drafted statuses."""
        # Test with drafted=0 (AVAILABLE)
        player_available = FantasyPlayer(
            id=3,
            name="Available Locked",
            team="KC",
            position="WR",
            bye_week=7,
            drafted=0,
            locked=1,
            score=65.0,
            fantasy_points=180.0
        )
        assert "[AVAILABLE] [LOCKED]" in str(player_available)

        # Test with drafted=1 (DRAFTED)
        player_drafted = FantasyPlayer(
            id=4,
            name="Drafted Locked",
            team="KC",
            position="TE",
            bye_week=7,
            drafted=1,
            locked=1,
            score=55.0,
            fantasy_points=150.0
        )
        assert "[DRAFTED] [LOCKED]" in str(player_drafted)

        # Test with drafted=2 (ROSTERED)
        player_rostered = FantasyPlayer(
            id=5,
            name="Rostered Locked",
            team="KC",
            position="K",
            bye_week=7,
            drafted=2,
            locked=1,
            score=45.0,
            fantasy_points=120.0
        )
        assert "[ROSTERED] [LOCKED]" in str(player_rostered)

    def test_str_locked_indicator_format(self):
        """Test that the full format includes [LOCKED] in correct position."""
        # Arrange
        player = FantasyPlayer(
            id=6,
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            bye_week=10,
            drafted=2,
            locked=1,
            score=92.3,
            fantasy_points=310.5,
            injury_status="ACTIVE"
        )

        # Act
        player_str = str(player)

        # Assert
        # Expected format: "Name (Team Position) - Score pts [Bye=X] [STATUS] [LOCKED]"
        assert "Patrick Mahomes" in player_str
        assert "(KC QB)" in player_str
        assert "92.3 pts" in player_str
        assert "[Bye=10]" in player_str
        assert "[ROSTERED]" in player_str
        assert "[LOCKED]" in player_str
        # Ensure [LOCKED] comes after [ROSTERED]
        assert player_str.index("[ROSTERED]") < player_str.index("[LOCKED]")


class TestFantasyPlayerInit:
    """Test suite for FantasyPlayer initialization."""

    def test_basic_initialization(self):
        """Test initialization with required fields only."""
        player = FantasyPlayer(
            id=1,
            name="Test Player",
            team="KC",
            position="QB"
        )

        assert player.id == 1
        assert player.name == "Test Player"
        assert player.team == "KC"
        assert player.position == "QB"
        assert player.drafted == 0  # Default
        assert player.locked == 0  # Default
        assert player.fantasy_points == 0.0  # Default

    def test_initialization_with_all_fields(self):
        """Test initialization with all available fields."""
        player = FantasyPlayer(
            id=2,
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            bye_week=7,
            drafted=2,
            locked=1,
            fantasy_points=310.5,
            average_draft_position=5.2,
            player_rating=95.8,
            week_1_points=25.3,
            injury_status="ACTIVE",
            score=92.5,
            weighted_projection=88.0,
            consistency=0.85,
            matchup_score=10,
            team_offensive_rank=3,
            team_defensive_rank=15
        )

        assert player.id == 2
        assert player.average_draft_position == 5.2
        assert player.player_rating == 95.8
        assert player.week_1_points == 25.3
        assert player.injury_status == "ACTIVE"
        assert player.team_offensive_rank == 3


class TestFromDict:
    """Test suite for from_dict() factory method."""

    def test_from_dict_with_valid_data(self):
        """Test from_dict with complete valid data."""
        data = {
            'id': 1,
            'name': 'Test Player',
            'team': 'KC',
            'position': 'QB',
            'bye_week': 7,
            'drafted': 0,
            'locked': 0,
            'fantasy_points': 250.0,
            'average_draft_position': 10.5
        }

        player = FantasyPlayer.from_dict(data)

        assert player.id == 1
        assert player.name == 'Test Player'
        assert player.team == 'KC'
        assert player.position == 'QB'
        assert player.bye_week == 7
        assert player.average_draft_position == 10.5

    def test_from_dict_with_missing_fields(self):
        """Test from_dict handles missing optional fields gracefully."""
        data = {
            'id': 2,
            'name': 'Minimal Player',
            'team': 'DAL',
            'position': 'RB'
        }

        player = FantasyPlayer.from_dict(data)

        assert player.id == 2
        assert player.name == 'Minimal Player'
        assert player.bye_week == 0  # Default from safe_int_conversion
        assert player.drafted == 0
        assert player.average_draft_position is None

    def test_from_dict_handles_string_numbers(self):
        """Test from_dict converts string numbers correctly."""
        data = {
            'id': '3',
            'name': 'String Data Player',
            'team': 'BUF',
            'position': 'WR',
            'bye_week': '9',
            'fantasy_points': '280.5',
            'average_draft_position': '15.3'
        }

        player = FantasyPlayer.from_dict(data)

        assert player.id == 3
        assert player.bye_week == 9
        assert player.fantasy_points == 280.5
        assert player.average_draft_position == 15.3

    def test_from_dict_handles_nan_values(self):
        """Test from_dict handles NaN/None/null values correctly."""
        data = {
            'id': 4,
            'name': 'NaN Player',
            'team': 'SF',
            'position': 'TE',
            'bye_week': 'nan',
            'average_draft_position': None,
            'player_rating': 'null'
        }

        player = FantasyPlayer.from_dict(data)

        assert player.id == 4
        assert player.bye_week == 0  # Default for NaN
        assert player.average_draft_position is None
        assert player.player_rating is None

    def test_from_dict_backward_compatibility_with_adp(self):
        """Test from_dict supports both 'adp' and 'average_draft_position' keys."""
        # Test with 'adp' key (old format)
        data_old = {
            'id': 5,
            'name': 'Old Format',
            'team': 'MIA',
            'position': 'QB',
            'adp': 8.5
        }

        player = FantasyPlayer.from_dict(data_old)
        assert player.average_draft_position == 8.5

        # Test with 'average_draft_position' key (new format)
        data_new = {
            'id': 6,
            'name': 'New Format',
            'team': 'MIA',
            'position': 'QB',
            'average_draft_position': 9.5
        }

        player = FantasyPlayer.from_dict(data_new)
        assert player.average_draft_position == 9.5


class TestPlayerMethods:
    """Test suite for FantasyPlayer helper methods."""

    def test_is_available_returns_true_when_not_drafted_not_locked(self):
        """Test is_available returns True for available players."""
        player = FantasyPlayer(
            id=1, name="Available", team="KC", position="QB",
            drafted=0, locked=0
        )

        assert player.is_available() is True

    def test_is_available_returns_false_when_drafted(self):
        """Test is_available returns False when player is drafted."""
        player = FantasyPlayer(
            id=2, name="Drafted", team="KC", position="QB",
            drafted=1, locked=0
        )

        assert player.is_available() is False

    def test_is_available_returns_false_when_locked(self):
        """Test is_available returns False when player is locked."""
        player = FantasyPlayer(
            id=3, name="Locked", team="KC", position="QB",
            drafted=0, locked=1
        )

        assert player.is_available() is False

    def test_is_rostered_returns_true_when_drafted_equals_two(self):
        """Test is_rostered returns True when drafted=2."""
        player = FantasyPlayer(
            id=4, name="Rostered", team="KC", position="QB",
            drafted=2
        )

        assert player.is_rostered() is True

    def test_is_rostered_returns_false_when_drafted_not_two(self):
        """Test is_rostered returns False when drafted != 2."""
        player = FantasyPlayer(
            id=5, name="Not Rostered", team="KC", position="QB",
            drafted=0
        )

        assert player.is_rostered() is False

    def test_is_locked_returns_true_when_locked_equals_one(self):
        """Test is_locked returns True when locked=1."""
        player = FantasyPlayer(
            id=6, name="Locked", team="KC", position="QB",
            locked=1
        )

        assert player.is_locked() is True

    def test_is_locked_returns_false_when_locked_equals_zero(self):
        """Test is_locked returns False when locked=0."""
        player = FantasyPlayer(
            id=7, name="Unlocked", team="KC", position="QB",
            locked=0
        )

        assert player.is_locked() is False


class TestRiskLevel:
    """Test suite for get_risk_level() method."""

    def test_get_risk_level_low_for_active(self):
        """Test get_risk_level returns LOW for ACTIVE players."""
        player = FantasyPlayer(
            id=1, name="Active", team="KC", position="QB",
            injury_status="ACTIVE"
        )

        assert player.get_risk_level() == "LOW"

    def test_get_risk_level_medium_for_questionable(self):
        """Test get_risk_level returns MEDIUM for QUESTIONABLE players."""
        player = FantasyPlayer(
            id=2, name="Questionable", team="KC", position="QB",
            injury_status="QUESTIONABLE"
        )

        assert player.get_risk_level() == "MEDIUM"

    def test_get_risk_level_high_for_out(self):
        """Test get_risk_level returns HIGH for OUT players."""
        player = FantasyPlayer(
            id=3, name="Out", team="KC", position="QB",
            injury_status="OUT"
        )

        assert player.get_risk_level() == "HIGH"

    def test_get_risk_level_high_for_injury_reserve(self):
        """Test get_risk_level returns HIGH for INJURY_RESERVE players."""
        player = FantasyPlayer(
            id=4, name="IR", team="KC", position="QB",
            injury_status="INJURY_RESERVE"
        )

        assert player.get_risk_level() == "HIGH"


class TestWeeklyProjections:
    """Test suite for weekly projection methods."""

    def test_get_weekly_projections_returns_all_weeks(self):
        """Test get_weekly_projections returns list of 17 weeks."""
        player = FantasyPlayer(
            id=1, name="Projected", team="KC", position="QB",
            week_1_points=25.0,
            week_2_points=22.5,
            week_17_points=30.0
        )

        projections = player.get_weekly_projections()

        assert len(projections) == 17
        assert projections[0] == 25.0  # Week 1
        assert projections[1] == 22.5  # Week 2
        assert projections[16] == 30.0  # Week 17

    def test_get_single_weekly_projection_returns_correct_week(self):
        """Test get_single_weekly_projection returns correct week value."""
        player = FantasyPlayer(
            id=2, name="Projected", team="KC", position="QB",
            week_5_points=28.5
        )

        assert player.get_single_weekly_projection(5) == 28.5

    def test_get_rest_of_season_projection_sums_remaining_weeks(self):
        """Test get_rest_of_season_projection sums from current week to week 17."""
        player = FantasyPlayer(
            id=3, name="Projected", team="KC", position="QB",
            week_1_points=20.0,
            week_2_points=25.0,
            week_3_points=22.0,
            week_4_points=24.0,
            week_5_points=26.0
        )

        # From week 3 to end (weeks 3, 4, 5 = 22 + 24 + 26 = 72)
        total = player.get_rest_of_season_projection(3)

        assert total == 72.0

    def test_get_rest_of_season_projection_handles_none_values(self):
        """Test get_rest_of_season_projection skips None weeks."""
        player = FantasyPlayer(
            id=4, name="Projected", team="KC", position="QB",
            week_1_points=20.0,
            week_2_points=None,  # Missing projection
            week_3_points=22.0
        )

        # From week 1 to end (weeks 1, 3 = 20 + 22 = 42, week 2 skipped)
        total = player.get_rest_of_season_projection(1)

        assert total == 42.0


class TestToDict:
    """Test suite for to_dict() method."""

    def test_to_dict_returns_dictionary(self):
        """Test to_dict returns all fields as dictionary."""
        player = FantasyPlayer(
            id=1,
            name="Test",
            team="KC",
            position="QB",
            drafted=2,
            locked=1,
            fantasy_points=250.0
        )

        player_dict = player.to_dict()

        assert isinstance(player_dict, dict)
        assert player_dict['id'] == 1
        assert player_dict['name'] == "Test"
        assert player_dict['team'] == "KC"
        assert player_dict['position'] == "QB"
        assert player_dict['drafted'] == 2
        assert player_dict['locked'] == 1
        assert player_dict['fantasy_points'] == 250.0


class TestRepr:
    """Test suite for __repr__() method."""

    def test_repr_shows_developer_representation(self):
        """Test __repr__ shows useful developer information."""
        player = FantasyPlayer(
            id=1,
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            fantasy_points=310.5
        )

        repr_str = repr(player)

        assert "FantasyPlayer" in repr_str
        assert "id='1'" in repr_str
        assert "name='Patrick Mahomes'" in repr_str
        assert "team='KC'" in repr_str
        assert "position='QB'" in repr_str
        assert "fantasy_points=310.5" in repr_str


class TestGetPositionIncludingFlex:
    """Test suite for get_position_including_flex() method."""

    def test_rb_returns_flex(self):
        """Test RB position returns FLEX."""
        player = FantasyPlayer(id=1, name="RB", team="KC", position="RB")
        assert player.get_position_including_flex() == 'FLEX'

    def test_wr_returns_flex(self):
        """Test WR position returns FLEX."""
        player = FantasyPlayer(id=2, name="WR", team="KC", position="WR")
        assert player.get_position_including_flex() == 'FLEX'

    def test_qb_returns_qb(self):
        """Test QB position returns QB (not FLEX)."""
        player = FantasyPlayer(id=3, name="QB", team="KC", position="QB")
        assert player.get_position_including_flex() == 'QB'

    def test_te_returns_te(self):
        """Test TE position returns TE (not FLEX)."""
        player = FantasyPlayer(id=4, name="TE", team="KC", position="TE")
        assert player.get_position_including_flex() == 'TE'


class TestEqualityAndHashing:
    """Test suite for __eq__() and __hash__() methods."""

    def test_players_with_same_id_are_equal(self):
        """Test players with same ID are considered equal."""
        player1 = FantasyPlayer(id=1, name="Player A", team="KC", position="QB")
        player2 = FantasyPlayer(id=1, name="Player B", team="DAL", position="RB")

        assert player1 == player2

    def test_players_with_different_id_are_not_equal(self):
        """Test players with different IDs are not equal."""
        player1 = FantasyPlayer(id=1, name="Player A", team="KC", position="QB")
        player2 = FantasyPlayer(id=2, name="Player A", team="KC", position="QB")

        assert player1 != player2

    def test_player_not_equal_to_non_player(self):
        """Test player is not equal to non-FantasyPlayer object."""
        player = FantasyPlayer(id=1, name="Player", team="KC", position="QB")

        assert player != "not a player"
        assert player != 1
        assert player != None

    def test_players_with_same_id_have_same_hash(self):
        """Test players with same ID have same hash."""
        player1 = FantasyPlayer(id=1, name="Player A", team="KC", position="QB")
        player2 = FantasyPlayer(id=1, name="Player B", team="DAL", position="RB")

        assert hash(player1) == hash(player2)

    def test_players_can_be_used_in_sets(self):
        """Test players can be used in sets (requires hashable)."""
        player1 = FantasyPlayer(id=1, name="Player 1", team="KC", position="QB")
        player2 = FantasyPlayer(id=2, name="Player 2", team="DAL", position="RB")
        player3 = FantasyPlayer(id=1, name="Player 1 Duplicate", team="KC", position="QB")

        player_set = {player1, player2, player3}

        # player1 and player3 have same ID, so only 2 unique players
        assert len(player_set) == 2


class TestAdpProperty:
    """Test suite for adp property (backward compatibility alias)."""

    def test_adp_getter_returns_average_draft_position(self):
        """Test adp property getter returns average_draft_position value."""
        player = FantasyPlayer(
            id=1, name="Test", team="KC", position="QB",
            average_draft_position=10.5
        )

        assert player.adp == 10.5

    def test_adp_setter_sets_average_draft_position(self):
        """Test adp property setter updates average_draft_position."""
        player = FantasyPlayer(
            id=2, name="Test", team="KC", position="QB"
        )

        player.adp = 15.3

        assert player.average_draft_position == 15.3
        assert player.adp == 15.3


class TestSafeConversionFunctions:
    """Test suite for safe_int_conversion and safe_float_conversion helper functions."""

    def test_safe_int_conversion_with_valid_int(self):
        """Test safe_int_conversion handles valid integers."""
        assert safe_int_conversion(5) == 5
        assert safe_int_conversion(0) == 0
        assert safe_int_conversion(-10) == -10

    def test_safe_int_conversion_with_valid_string(self):
        """Test safe_int_conversion handles string integers."""
        assert safe_int_conversion("5") == 5
        assert safe_int_conversion("100") == 100

    def test_safe_int_conversion_with_float(self):
        """Test safe_int_conversion converts floats to ints."""
        assert safe_int_conversion(5.7) == 5
        assert safe_int_conversion("10.9") == 10

    def test_safe_int_conversion_with_invalid_values(self):
        """Test safe_int_conversion returns default for invalid values."""
        assert safe_int_conversion(None) is None
        assert safe_int_conversion("") is None
        assert safe_int_conversion("nan") is None
        assert safe_int_conversion("invalid", default=0) == 0

    def test_safe_float_conversion_with_valid_float(self):
        """Test safe_float_conversion handles valid floats."""
        assert safe_float_conversion(5.5) == 5.5
        assert safe_float_conversion(0.0) == 0.0
        assert safe_float_conversion(-10.3) == -10.3

    def test_safe_float_conversion_with_valid_string(self):
        """Test safe_float_conversion handles string floats."""
        assert safe_float_conversion("5.5") == 5.5
        assert safe_float_conversion("100.75") == 100.75

    def test_safe_float_conversion_with_invalid_values(self):
        """Test safe_float_conversion returns default for invalid values."""
        assert safe_float_conversion(None) == 0.0
        assert safe_float_conversion("") == 0.0
        assert safe_float_conversion("nan") == 0.0
        assert safe_float_conversion("invalid", default=1.0) == 1.0

    def test_safe_int_conversion_handles_infinity(self):
        """Test safe_int_conversion rejects infinity values."""
        assert safe_int_conversion(float('inf'), default=0) == 0
        assert safe_int_conversion(float('-inf'), default=0) == 0

    def test_safe_float_conversion_handles_infinity(self):
        """Test safe_float_conversion rejects infinity values."""
        assert safe_float_conversion(float('inf'), default=0.0) == 0.0
        assert safe_float_conversion(float('-inf'), default=0.0) == 0.0
