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
            drafted_by="",
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
            drafted_by="",
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
            drafted_by="",
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
            drafted_by="Opponent Team",
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
            drafted_by="Sea Sharp",
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
            drafted_by="Sea Sharp",
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
        assert player.is_free_agent()  # Default
        assert player.locked == 0  # Default
        assert player.fantasy_points == 0.0  # Default

    def test_initialization_with_all_fields(self):
        """Test initialization with all available fields (UPDATED for Sub-feature 2)."""
        player = FantasyPlayer(
            id=2,
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            bye_week=7,
            drafted_by="Sea Sharp",
            locked=1,
            fantasy_points=310.5,
            average_draft_position=5.2,
            player_rating=95.8,
            projected_points=[25.3] * 17,  # Array-based (Sub-feature 1)
            actual_points=[0.0] * 17,      # Array-based (Sub-feature 1)
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
        assert player.projected_points[0] == 25.3  # Array-based (Sub-feature 1)
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
        assert player.is_free_agent()
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
            drafted_by="", locked=0
        )

        assert player.is_available() is True

    def test_is_available_returns_false_when_drafted(self):
        """Test is_available returns False when player is drafted."""
        player = FantasyPlayer(
            id=2, name="Drafted", team="KC", position="QB",
            drafted_by="Opponent Team", locked=0
        )

        assert player.is_available() is False

    def test_is_available_returns_false_when_locked(self):
        """Test is_available returns False when player is locked."""
        player = FantasyPlayer(
            id=3, name="Locked", team="KC", position="QB",
            drafted_by="", locked=1
        )

        assert player.is_available() is False

    def test_is_rostered_returns_true_when_drafted_equals_two(self):
        """Test is_rostered returns True when drafted_by is our team."""
        player = FantasyPlayer(
            id=4, name="Rostered", team="KC", position="QB",
            drafted_by="Sea Sharp"
        )

        assert player.is_rostered() is True

    def test_is_rostered_returns_false_when_drafted_not_two(self):
        """Test is_rostered returns False when drafted != 2."""
        player = FantasyPlayer(
            id=5, name="Not Rostered", team="KC", position="QB",
            drafted_by=""
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
        """Test get_risk_level returns MEDIUM for OUT players."""
        player = FantasyPlayer(
            id=3, name="Out", team="KC", position="QB",
            injury_status="OUT"
        )

        assert player.get_risk_level() == "MEDIUM"

    def test_get_risk_level_high_for_injury_reserve(self):
        """Test get_risk_level returns HIGH for INJURY_RESERVE players."""
        player = FantasyPlayer(
            id=4, name="IR", team="KC", position="QB",
            injury_status="INJURY_RESERVE"
        )

        assert player.get_risk_level() == "HIGH"


class TestWeeklyProjections:
    """Test suite for weekly projection methods (UPDATED for Sub-feature 2: hybrid logic)."""

    @pytest.fixture
    def mock_config(self):
        """Create mock config with current_nfl_week."""
        class MockConfig:
            def __init__(self, current_week):
                self.current_nfl_week = current_week
        return MockConfig

    def test_get_weekly_projections_returns_all_weeks(self, mock_config):
        """Test get_weekly_projections returns list of 17 weeks with hybrid logic."""
        # Create projected points array
        projected = [0.0] * 17
        projected[0] = 25.0   # Week 1
        projected[1] = 22.5   # Week 2
        projected[16] = 30.0  # Week 17

        player = FantasyPlayer(
            id=1, name="Projected", team="KC", position="QB",
            projected_points=projected,
            actual_points=[0.0] * 17
        )

        config = mock_config(current_week=1)  # Week 1, so all projected
        projections = player.get_weekly_projections(config)

        assert len(projections) == 17
        assert projections[0] == 25.0  # Week 1
        assert projections[1] == 22.5  # Week 2
        assert projections[16] == 30.0  # Week 17

    def test_get_single_weekly_projection_returns_correct_week(self, mock_config):
        """Test get_single_weekly_projection returns correct week value."""
        projected = [0.0] * 17
        projected[4] = 28.5  # Week 5

        player = FantasyPlayer(
            id=2, name="Projected", team="KC", position="QB",
            projected_points=projected,
            actual_points=[0.0] * 17
        )

        config = mock_config(current_week=1)
        assert player.get_single_weekly_projection(5, config) == 28.5

    def test_get_rest_of_season_projection_sums_remaining_weeks(self, mock_config):
        """Test get_rest_of_season_projection sums from current week to week 17."""
        projected = [0.0] * 17
        projected[0] = 20.0  # Week 1
        projected[1] = 25.0  # Week 2
        projected[2] = 22.0  # Week 3
        projected[3] = 24.0  # Week 4
        projected[4] = 26.0  # Week 5

        player = FantasyPlayer(
            id=3, name="Projected", team="KC", position="QB",
            projected_points=projected,
            actual_points=[0.0] * 17
        )

        config = mock_config(current_week=3)
        # From week 3 to end (weeks 3, 4, 5 = 22 + 24 + 26 = 72)
        total = player.get_rest_of_season_projection(config)

        assert total == 72.0

    def test_get_rest_of_season_projection_handles_none_values(self, mock_config):
        """Test get_rest_of_season_projection skips None weeks."""
        projected = [0.0] * 17
        projected[0] = 20.0  # Week 1
        projected[1] = None  # Week 2 - Missing projection
        projected[2] = 22.0  # Week 3

        player = FantasyPlayer(
            id=4, name="Projected", team="KC", position="QB",
            projected_points=projected,
            actual_points=[0.0] * 17
        )

        config = mock_config(current_week=1)
        # From week 1 to end (weeks 1, 3 = 20 + 22 = 42, week 2 skipped)
        total = player.get_rest_of_season_projection(config)

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
            drafted_by="Sea Sharp",
            locked=1,
            fantasy_points=250.0
        )

        player_dict = player.to_dict()

        assert isinstance(player_dict, dict)
        assert player_dict['id'] == 1
        assert player_dict['name'] == "Test"
        assert player_dict['team'] == "KC"
        assert player_dict['position'] == "QB"
        assert player_dict['drafted_by'] == "Sea Sharp"
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


class TestFantasyPlayerFromJSON:
    """Test suite for FantasyPlayer.from_json() method - Task 4.1, 4.2, 4.3"""

    def test_from_json_with_complete_qb_data(self):
        """Test from_json() loads QB with all fields populated."""
        # Arrange - Complete QB data with all stats
        json_data = {
            "id": "12345",
            "name": "Patrick Mahomes",
            "team": "KC",
            "position": "QB",
            "bye_week": 7,
            "drafted_by": "",
            "locked": False,
            "average_draft_position": 15.3,
            "player_rating": 95.5,
            "injury_status": "ACTIVE",
            "projected_points": [25.3, 28.1, 22.5] + [20.0] * 14,
            "actual_points": [0.0] * 17,
            "passing": {
                "completions": [22.5] * 17,
                "attempts": [35.0] * 17,
                "pass_yds": [320.0] * 17,
                "pass_tds": [2.5] * 17
            },
            "rushing": {
                "rush_att": [3.0] * 17,
                "rush_yds": [15.0] * 17,
                "rush_tds": [0.1] * 17
            },
            "misc": {
                "fumbles_lost": [0.2] * 17
            }
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert - Core fields
        assert player.id == 12345
        assert player.name == "Patrick Mahomes"
        assert player.team == "KC"
        assert player.position == "QB"
        assert player.bye_week == 7
        assert player.is_free_agent()  # Empty drafted_by → 0
        assert player.locked == False
        assert player.average_draft_position == 15.3
        assert player.player_rating == 95.5
        assert player.injury_status == "ACTIVE"

        # Assert - Arrays
        assert len(player.projected_points) == 17
        assert player.projected_points[0] == 25.3
        assert player.projected_points[1] == 28.1
        assert len(player.actual_points) == 17
        assert player.actual_points[0] == 0.0

        # Assert - Calculated fantasy_points
        expected_fantasy_points = sum([25.3, 28.1, 22.5] + [20.0] * 14)
        assert player.fantasy_points == expected_fantasy_points

        # Assert - Position-specific stats
        assert player.passing is not None
        assert player.passing["completions"] == [22.5] * 17
        assert player.rushing is not None
        assert player.misc is not None
        assert player.receiving is None  # QB doesn't have receiving
        assert player.defense is None  # QB doesn't have defense

    def test_from_json_with_partial_rb_data(self):
        """Test from_json() loads RB with partial fields (verify Optional fields = None)."""
        # Arrange - Minimal RB data
        json_data = {
            "id": "67890",
            "name": "Christian McCaffrey",
            "team": "SF",
            "position": "RB",
            "projected_points": [18.5] * 17,
            "actual_points": [0.0] * 17,
            "rushing": {
                "rush_att": [20.0] * 17,
                "rush_yds": [95.0] * 17,
                "rush_tds": [0.8] * 17
            },
            "receiving": {
                "receptions": [4.5] * 17,
                "rec_yds": [35.0] * 17,
                "rec_tds": [0.2] * 17
            }
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert - Core fields with defaults
        assert player.id == 67890
        assert player.name == "Christian McCaffrey"
        assert player.bye_week is None  # Not provided
        assert player.is_free_agent()  # Default (no drafted_by)
        assert player.locked == False  # Default
        assert player.average_draft_position is None  # Not provided
        assert player.injury_status == "UNKNOWN"  # Default

        # Assert - Position-specific stats
        assert player.rushing is not None
        assert player.receiving is not None
        assert player.passing is None  # RB doesn't have passing
        assert player.defense is None

    def test_from_json_with_kicker_no_passing_rushing(self):
        """Test from_json() loads K without passing/rushing stats."""
        # Arrange - Kicker data
        json_data = {
            "id": "11111",
            "name": "Justin Tucker",
            "team": "BAL",
            "position": "K",
            "projected_points": [9.5] * 17,
            "actual_points": [0.0] * 17,
            "field_goals": {
                "fg_made": [2.5] * 17,
                "fg_att": [3.0] * 17
            },
            "extra_points": {
                "xp_made": [3.5] * 17,
                "xp_att": [4.0] * 17
            }
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert
        assert player.position == "K"
        assert player.field_goals is not None
        assert player.extra_points is not None
        assert player.passing is None
        assert player.rushing is None
        assert player.receiving is None
        assert player.defense is None

    def test_from_json_with_dst_defense_stats(self):
        """Test from_json() loads DST with defense stats."""
        # Arrange - DST data
        json_data = {
            "id": "99999",
            "name": "San Francisco",
            "team": "SF",
            "position": "DST",
            "projected_points": [10.5] * 17,
            "actual_points": [0.0] * 17,
            "defense": {
                "sacks": [3.0] * 17,
                "interceptions": [1.5] * 17,
                "fumbles_recovered": [0.8] * 17,
                "touchdowns": [0.3] * 17,
                "points_allowed": [18.5] * 17
            }
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert
        assert player.position == "DST"
        assert player.defense is not None
        assert player.defense["sacks"] == [3.0] * 17
        assert player.passing is None
        assert player.rushing is None
        assert player.field_goals is None

    def test_from_json_id_conversion_string_to_int(self):
        """Test from_json() converts id from string to int."""
        # Arrange
        json_data = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC",
            "position": "QB"
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert
        assert isinstance(player.id, int)
        assert player.id == 12345

    def test_from_json_drafted_by_conversion_undrafted(self):
        """Test from_json() converts drafted_by empty string to drafted=0."""
        # Arrange
        json_data = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC",
            "position": "QB",
            "drafted_by": ""
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert
        assert player.is_free_agent()

    def test_from_json_drafted_by_conversion_our_team(self):
        """Test from_json() loads drafted_by='Sea Sharp' correctly."""
        # Arrange
        json_data = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC",
            "position": "QB",
            "drafted_by": "Sea Sharp"
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert - verify drafted_by is loaded
        assert player.drafted_by == "Sea Sharp"
        # Note: drafted property derivation will be tested in Phase 4 (REQ-016)

    def test_from_json_drafted_by_conversion_other_team(self):
        """Test from_json() loads drafted_by='Opponent Team' correctly."""
        # Arrange
        json_data = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC",
            "position": "QB",
            "drafted_by": "Opponent Team"
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert - verify drafted_by is loaded
        assert player.drafted_by == "Opponent Team"
        # Note: drafted property derivation will be tested in Phase 4 (REQ-016)

    def test_from_json_locked_boolean_loading(self):
        """Test from_json() loads locked as boolean directly."""
        # Arrange
        json_data_locked = {
            "id": "12345",
            "name": "Locked Player",
            "team": "KC",
            "position": "QB",
            "locked": True
        }
        json_data_unlocked = {
            "id": "67890",
            "name": "Unlocked Player",
            "team": "KC",
            "position": "QB",
            "locked": False
        }

        # Act
        player_locked = FantasyPlayer.from_json(json_data_locked)
        player_unlocked = FantasyPlayer.from_json(json_data_unlocked)

        # Assert
        assert player_locked.locked == True
        assert player_unlocked.locked == False

    def test_from_json_fantasy_points_calculated_from_projected_points(self):
        """Test from_json() calculates fantasy_points as sum of projected_points."""
        # Arrange
        projected = [25.0, 28.0, 22.0] + [20.0] * 14
        json_data = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC",
            "position": "QB",
            "projected_points": projected
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert
        expected_sum = sum(projected)
        assert player.fantasy_points == expected_sum

    def test_from_json_array_padding_short_array(self):
        """Test from_json() pads arrays with less than 17 elements."""
        # Arrange - Only 15 elements
        json_data = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC",
            "position": "QB",
            "projected_points": [25.0] * 15,
            "actual_points": [10.0] * 10
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert
        assert len(player.projected_points) == 17
        assert len(player.actual_points) == 17
        assert player.projected_points[14] == 25.0
        assert player.projected_points[15] == 0.0  # Padded
        assert player.projected_points[16] == 0.0  # Padded
        assert player.actual_points[9] == 10.0
        assert player.actual_points[10] == 0.0  # Padded

    def test_from_json_array_truncation_long_array(self):
        """Test from_json() truncates arrays with more than 17 elements."""
        # Arrange - 20 elements
        json_data = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC",
            "position": "QB",
            "projected_points": [25.0] * 20,
            "actual_points": [10.0] * 18
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert
        assert len(player.projected_points) == 17
        assert len(player.actual_points) == 17

    def test_from_json_missing_arrays_default_to_zeros(self):
        """Test from_json() creates default [0.0]*17 arrays when missing."""
        # Arrange - No arrays provided
        json_data = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC",
            "position": "QB"
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert
        assert len(player.projected_points) == 17
        assert len(player.actual_points) == 17
        assert all(p == 0.0 for p in player.projected_points)
        assert all(p == 0.0 for p in player.actual_points)

    def test_from_json_empty_arrays(self):
        """Test from_json() handles empty arrays by padding to 17."""
        # Arrange
        json_data = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC",
            "position": "QB",
            "projected_points": [],
            "actual_points": []
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert
        assert len(player.projected_points) == 17
        assert len(player.actual_points) == 17
        assert all(p == 0.0 for p in player.projected_points)

    def test_from_json_missing_required_field_raises_value_error(self):
        """Test from_json() raises ValueError when required field is missing."""
        # Arrange - Missing 'name'
        json_data_no_name = {
            "id": "12345",
            "team": "KC",
            "position": "QB"
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Missing required field"):
            FantasyPlayer.from_json(json_data_no_name)

        # Arrange - Missing 'id'
        json_data_no_id = {
            "name": "Test Player",
            "team": "KC",
            "position": "QB"
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Missing required field"):
            FantasyPlayer.from_json(json_data_no_id)

        # Arrange - Missing 'position'
        json_data_no_position = {
            "id": "12345",
            "name": "Test Player",
            "team": "KC"
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Missing required field"):
            FantasyPlayer.from_json(json_data_no_position)

    def test_from_json_nested_stats_preservation(self):
        """Test from_json() preserves nested stat dictionaries exactly."""
        # Arrange
        passing_stats = {
            "completions": [22.5] * 17,
            "attempts": [35.0] * 17,
            "pass_yds": [320.0] * 17,
            "pass_tds": [2.5] * 17,
            "interceptions": [0.8] * 17
        }
        json_data = {
            "id": "12345",
            "name": "Test QB",
            "team": "KC",
            "position": "QB",
            "passing": passing_stats
        }

        # Act
        player = FantasyPlayer.from_json(json_data)

        # Assert - Nested dict preserved exactly
        assert player.passing == passing_stats
        assert player.passing["completions"] == [22.5] * 17
        assert player.passing["interceptions"] == [0.8] * 17


class TestFantasyPlayerHybridWeeklyData:
    """Test suite for hybrid weekly data methods (Sub-feature 2: Weekly Data Migration)."""

    @pytest.fixture
    def mock_config(self):
        """Create mock config with current_nfl_week."""
        class MockConfig:
            def __init__(self, current_week):
                self.current_nfl_week = current_week
        return MockConfig

    @pytest.fixture
    def sample_player(self):
        """Create player with different projected vs actual points."""
        return FantasyPlayer(
            id=1,
            name="Test Player",
            team="KC",
            position="QB",
            bye_week=7,
            projected_points=[10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0],
            actual_points=[15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0, 105.0, 115.0, 125.0, 135.0, 145.0, 155.0, 165.0, 175.0],
            fantasy_points=100.0
        )

    def test_get_weekly_projections_hybrid_past_weeks(self, sample_player, mock_config):
        """Test get_weekly_projections() returns actual for past weeks."""
        # Arrange
        config = mock_config(current_week=5)

        # Act
        result = sample_player.get_weekly_projections(config)

        # Assert - Past weeks (1-4) use actual_points
        assert result[0] == 15.0  # Week 1 - actual
        assert result[1] == 25.0  # Week 2 - actual
        assert result[2] == 35.0  # Week 3 - actual
        assert result[3] == 45.0  # Week 4 - actual

        # Assert - Current/future weeks (5-17) use projected_points
        assert result[4] == 50.0   # Week 5 - projected
        assert result[5] == 60.0   # Week 6 - projected
        assert result[16] == 170.0 # Week 17 - projected

    def test_get_weekly_projections_hybrid_at_current_week_boundary(self, sample_player, mock_config):
        """Test get_weekly_projections() at current week boundary."""
        # Arrange
        config = mock_config(current_week=10)

        # Act
        result = sample_player.get_weekly_projections(config)

        # Assert - Week 9 (past) uses actual
        assert result[8] == 95.0  # Week 9 - actual

        # Assert - Week 10 (current) uses projected
        assert result[9] == 100.0 # Week 10 - projected

    def test_get_weekly_projections_edge_case_week_1(self, sample_player, mock_config):
        """Test get_weekly_projections() when current_week=1 (all projected)."""
        # Arrange
        config = mock_config(current_week=1)

        # Act
        result = sample_player.get_weekly_projections(config)

        # Assert - All weeks use projected (no past weeks)
        assert result[0] == 10.0   # Week 1 - projected
        assert result[8] == 90.0   # Week 9 - projected
        assert result[16] == 170.0 # Week 17 - projected

    def test_get_weekly_projections_edge_case_week_18(self, sample_player, mock_config):
        """Test get_weekly_projections() when current_week=18 (all actual)."""
        # Arrange
        config = mock_config(current_week=18)

        # Act
        result = sample_player.get_weekly_projections(config)

        # Assert - All weeks use actual (all are past)
        assert result[0] == 15.0   # Week 1 - actual
        assert result[8] == 95.0   # Week 9 - actual
        assert result[16] == 175.0 # Week 17 - actual

    def test_get_single_weekly_projection_with_config(self, sample_player, mock_config):
        """Test get_single_weekly_projection() delegates to hybrid logic."""
        # Arrange
        config = mock_config(current_week=8)

        # Act - Past week
        past_result = sample_player.get_single_weekly_projection(5, config)
        # Act - Future week
        future_result = sample_player.get_single_weekly_projection(12, config)

        # Assert
        assert past_result == 55.0   # Week 5 is past - uses actual
        assert future_result == 120.0 # Week 12 is future - uses projected

    def test_get_single_weekly_projection_validation_week_0(self, sample_player, mock_config):
        """Test get_single_weekly_projection() raises ValueError for week_num=0."""
        # Arrange
        config = mock_config(current_week=5)

        # Act & Assert
        with pytest.raises(ValueError, match="week_num must be between 1 and 17"):
            sample_player.get_single_weekly_projection(0, config)

    def test_get_single_weekly_projection_validation_week_negative(self, sample_player, mock_config):
        """Test get_single_weekly_projection() raises ValueError for negative week_num."""
        # Arrange
        config = mock_config(current_week=5)

        # Act & Assert
        with pytest.raises(ValueError, match="week_num must be between 1 and 17"):
            sample_player.get_single_weekly_projection(-1, config)

    def test_get_single_weekly_projection_validation_week_18(self, sample_player, mock_config):
        """Test get_single_weekly_projection() raises ValueError for week_num=18."""
        # Arrange
        config = mock_config(current_week=5)

        # Act & Assert
        with pytest.raises(ValueError, match="week_num must be between 1 and 17"):
            sample_player.get_single_weekly_projection(18, config)

    def test_get_rest_of_season_projection_with_config(self, sample_player, mock_config):
        """Test get_rest_of_season_projection() uses hybrid data."""
        # Arrange
        config = mock_config(current_week=10)

        # Act
        result = sample_player.get_rest_of_season_projection(config)

        # Assert - Sum of weeks 10-17 (all projected since week 10 is current)
        # Weeks 10-17: 100.0 + 110.0 + 120.0 + 130.0 + 140.0 + 150.0 + 160.0 + 170.0
        expected = 100.0 + 110.0 + 120.0 + 130.0 + 140.0 + 150.0 + 160.0 + 170.0
        assert result == expected

    def test_get_rest_of_season_projection_includes_current_week_actual(self, sample_player, mock_config):
        """Test ROS projection uses actual if current week already played."""
        # Arrange
        config = mock_config(current_week=6)

        # Act
        result = sample_player.get_rest_of_season_projection(config)

        # Assert - Sum of weeks 6-17 (week 6+ use projected)
        # Weeks 6-17: 60.0 + 70.0 + 80.0 + 90.0 + 100.0 + 110.0 + 120.0 + 130.0 + 140.0 + 150.0 + 160.0 + 170.0
        expected = sum([60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0])
        assert result == expected
