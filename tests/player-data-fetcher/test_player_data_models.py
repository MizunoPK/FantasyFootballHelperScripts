"""
Unit tests for player_data_models module

Tests Pydantic models, validation, and data manipulation methods.

Author: Kai Mizuno
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

from player_data_models import (
    ScoringFormat,
    ESPNPlayerData,
    PlayerProjection,
    ProjectionData,
    DataCollectionError,
    PlayerDataValidationError
)


class TestScoringFormat:
    """Test ScoringFormat enum"""

    def test_scoring_format_standard(self):
        """Test STANDARD scoring format value"""
        assert ScoringFormat.STANDARD == "std"
        assert ScoringFormat.STANDARD.value == "std"

    def test_scoring_format_ppr(self):
        """Test PPR scoring format value"""
        assert ScoringFormat.PPR == "ppr"
        assert ScoringFormat.PPR.value == "ppr"

    def test_scoring_format_half_ppr(self):
        """Test HALF_PPR scoring format value"""
        assert ScoringFormat.HALF_PPR == "half"
        assert ScoringFormat.HALF_PPR.value == "half"

    def test_scoring_format_enum_membership(self):
        """Test ScoringFormat enum membership"""
        assert "std" in [sf.value for sf in ScoringFormat]
        assert "ppr" in [sf.value for sf in ScoringFormat]
        assert "half" in [sf.value for sf in ScoringFormat]


class TestESPNPlayerDataInitialization:
    """Test ESPNPlayerData model initialization"""

    def test_init_with_required_fields_only(self):
        """Test initialization with only required fields"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )

        assert player.id == "12345"
        assert player.name == "Test Player"
        assert player.team == "TB"
        assert player.position == "QB"

    def test_init_with_all_fields(self):
        """Test initialization with all fields"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB",
            bye_week=7,
            drafted_by="Opponent Team",
            locked=0,
            fantasy_points=250.5,
            average_draft_position=3.2,
            player_rating=95.0,
            injury_status="QUESTIONABLE"
        )

        assert player.bye_week == 7
        assert player.drafted_by == "Opponent Team"
        assert player.fantasy_points == 250.5
        assert player.average_draft_position == 3.2
        assert player.injury_status == "QUESTIONABLE"

    def test_init_default_values(self):
        """Test default values for optional fields"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )

        assert player.bye_week is None
        assert player.drafted_by == ""
        assert player.locked == 0
        assert player.fantasy_points == 0.0
        assert player.average_draft_position is None
        assert player.player_rating is None
        assert player.injury_status == "ACTIVE"
        assert player.api_source == "ESPN"

    def test_init_validates_required_fields(self):
        """Test that missing required fields raise ValidationError"""
        with pytest.raises(ValidationError):
            ESPNPlayerData(
                name="Test Player",
                team="TB"
                # Missing id and position
            )

    def test_init_sets_updated_at(self):
        """Test that updated_at is automatically set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )

        assert isinstance(player.updated_at, datetime)
        assert player.updated_at <= datetime.now()


class TestESPNPlayerDataWeeklyPoints:
    """Test weekly points methods"""

    def test_set_week_points_valid_week(self):
        """Test setting points for a valid week"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )

        player.set_week_points(5, 25.5)

        assert player.week_5_points == 25.5

    def test_set_week_points_all_weeks(self):
        """Test setting points for all 17 weeks"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="RB"
        )

        for week in range(1, 18):
            player.set_week_points(week, float(week * 10))

        for week in range(1, 18):
            assert player.get_week_points(week) == float(week * 10)

    def test_set_week_points_invalid_week_low(self):
        """Test setting points for week < 1 is ignored"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="WR"
        )

        player.set_week_points(0, 25.5)

        # Should not set anything
        assert not hasattr(player, 'week_0_points')

    def test_set_week_points_invalid_week_high(self):
        """Test setting points for week > 17 is ignored"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="TE"
        )

        player.set_week_points(18, 25.5)

        # Should not set anything
        assert not hasattr(player, 'week_18_points')

    def test_get_week_points_set_value(self):
        """Test getting points for a week that was set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )

        player.set_week_points(10, 30.2)

        assert player.get_week_points(10) == 30.2

    def test_get_week_points_unset_value(self):
        """Test getting points for a week that was not set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="RB"
        )

        assert player.get_week_points(5) is None

    def test_get_week_points_invalid_week_low(self):
        """Test getting points for week < 1 returns None"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="WR"
        )

        assert player.get_week_points(0) is None

    def test_get_week_points_invalid_week_high(self):
        """Test getting points for week > 17 returns None"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="TE"
        )

        assert player.get_week_points(18) is None

    def test_get_all_weekly_points_no_points_set(self):
        """Test getting all weekly points when none are set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="K"
        )

        all_points = player.get_all_weekly_points()

        assert len(all_points) == 17
        assert all(all_points[week] is None for week in range(1, 18))

    def test_get_all_weekly_points_some_points_set(self):
        """Test getting all weekly points when some are set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="DST"
        )

        player.set_week_points(1, 10.0)
        player.set_week_points(5, 20.0)
        player.set_week_points(10, 30.0)

        all_points = player.get_all_weekly_points()

        assert all_points[1] == 10.0
        assert all_points[5] == 20.0
        assert all_points[10] == 30.0
        assert all_points[2] is None
        assert all_points[17] is None

    def test_get_all_weekly_points_all_points_set(self):
        """Test getting all weekly points when all are set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )

        for week in range(1, 18):
            player.set_week_points(week, float(week * 5))

        all_points = player.get_all_weekly_points()

        assert len(all_points) == 17
        for week in range(1, 18):
            assert all_points[week] == float(week * 5)


class TestESPNPlayerDataValidation:
    """Test Pydantic validation"""

    def test_validates_drafted_by_is_string(self):
        """Test that drafted_by field accepts strings"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB",
            drafted_by="My Team"
        )

        assert player.drafted_by == "My Team"
        assert isinstance(player.drafted_by, str)

    def test_validates_fantasy_points_is_float(self):
        """Test that fantasy_points field accepts floats"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="RB",
            fantasy_points=125.75
        )

        assert player.fantasy_points == 125.75

    def test_converts_int_to_float_for_fantasy_points(self):
        """Test Pydantic converts int to float"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="TE",
            fantasy_points=100  # Int
        )

        assert player.fantasy_points == 100.0
        assert isinstance(player.fantasy_points, float)


class TestPlayerProjection:
    """Test PlayerProjection legacy model"""

    def test_player_projection_is_subclass(self):
        """Test PlayerProjection inherits from ESPNPlayerData"""
        assert issubclass(PlayerProjection, ESPNPlayerData)

    def test_player_projection_initialization(self):
        """Test PlayerProjection can be initialized like ESPNPlayerData"""
        player = PlayerProjection(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )

        assert player.id == "12345"
        assert player.name == "Test Player"

    def test_player_projection_has_all_methods(self):
        """Test PlayerProjection has all ESPNPlayerData methods"""
        player = PlayerProjection(
            id="12345",
            name="Test Player",
            team="TB",
            position="RB"
        )

        player.set_week_points(5, 25.0)
        assert player.get_week_points(5) == 25.0
        assert hasattr(player, 'get_all_weekly_points')


class TestProjectionData:
    """Test ProjectionData container model"""

    def test_projection_data_initialization(self):
        """Test ProjectionData initialization with required fields"""
        players = [
            ESPNPlayerData(id="1", name="Player 1", team="TB", position="QB"),
            ESPNPlayerData(id="2", name="Player 2", team="KC", position="RB")
        ]

        projection_data = ProjectionData(
            season=2024,
            scoring_format="ppr",
            total_players=2,
            players=players
        )

        assert projection_data.season == 2024
        assert projection_data.scoring_format == "ppr"
        assert projection_data.total_players == 2
        assert len(projection_data.players) == 2

    def test_projection_data_validates_required_fields(self):
        """Test ProjectionData requires all fields"""
        with pytest.raises(ValidationError):
            ProjectionData(
                season=2024,
                scoring_format="ppr"
                # Missing total_players and players
            )

    def test_projection_data_sets_generated_at(self):
        """Test ProjectionData sets generated_at automatically"""
        players = [
            ESPNPlayerData(id="1", name="Player 1", team="TB", position="QB")
        ]

        projection_data = ProjectionData(
            season=2024,
            scoring_format="std",
            total_players=1,
            players=players
        )

        assert isinstance(projection_data.generated_at, datetime)
        assert projection_data.generated_at <= datetime.now()

    def test_projection_data_with_empty_players_list(self):
        """Test ProjectionData with empty players list"""
        projection_data = ProjectionData(
            season=2024,
            scoring_format="half",
            total_players=0,
            players=[]
        )

        assert projection_data.total_players == 0
        assert len(projection_data.players) == 0

    def test_projection_data_total_players_mismatch(self):
        """Test ProjectionData allows total_players != len(players)"""
        # Pydantic doesn't enforce this relationship by default
        players = [
            ESPNPlayerData(id="1", name="Player 1", team="TB", position="QB")
        ]

        projection_data = ProjectionData(
            season=2024,
            scoring_format="ppr",
            total_players=100,  # Doesn't match len(players)
            players=players
        )

        assert projection_data.total_players == 100
        assert len(projection_data.players) == 1


class TestCustomExceptions:
    """Test custom exception classes"""

    def test_data_collection_error_is_exception(self):
        """Test DataCollectionError is an Exception"""
        assert issubclass(DataCollectionError, Exception)

    def test_data_collection_error_can_be_raised(self):
        """Test DataCollectionError can be raised and caught"""
        with pytest.raises(DataCollectionError):
            raise DataCollectionError("Test error")

    def test_data_collection_error_with_message(self):
        """Test DataCollectionError stores message"""
        try:
            raise DataCollectionError("Test error message")
        except DataCollectionError as e:
            assert str(e) == "Test error message"

    def test_player_data_validation_error_is_exception(self):
        """Test PlayerDataValidationError is an Exception"""
        assert issubclass(PlayerDataValidationError, Exception)

    def test_player_data_validation_error_can_be_raised(self):
        """Test PlayerDataValidationError can be raised and caught"""
        with pytest.raises(PlayerDataValidationError):
            raise PlayerDataValidationError("Validation failed")

    def test_player_data_validation_error_with_message(self):
        """Test PlayerDataValidationError stores message"""
        try:
            raise PlayerDataValidationError("Invalid player data")
        except PlayerDataValidationError as e:
            assert str(e) == "Invalid player data"


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_espn_player_data_with_zero_fantasy_points(self):
        """Test player with zero fantasy points"""
        player = ESPNPlayerData(
            id="12345",
            name="Backup Player",
            team="TB",
            position="QB",
            fantasy_points=0.0
        )

        assert player.fantasy_points == 0.0

    def test_espn_player_data_with_negative_fantasy_points(self):
        """Test player with negative fantasy points (DST)"""
        player = ESPNPlayerData(
            id="12345",
            name="Bad Defense",
            team="TB",
            position="DST",
            fantasy_points=-5.0
        )

        assert player.fantasy_points == -5.0

    def test_espn_player_data_with_very_high_adp(self):
        """Test player with very high ADP (late pick)"""
        player = ESPNPlayerData(
            id="12345",
            name="Late Round Pick",
            team="TB",
            position="K",
            average_draft_position=200.5
        )

        assert player.average_draft_position == 200.5

    def test_espn_player_data_with_bye_week_boundaries(self):
        """Test bye week at boundaries"""
        player1 = ESPNPlayerData(
            id="1", name="Early Bye", team="TB", position="QB", bye_week=4
        )
        player2 = ESPNPlayerData(
            id="2", name="Late Bye", team="KC", position="RB", bye_week=14
        )

        assert player1.bye_week == 4
        assert player2.bye_week == 14

    def test_espn_player_data_with_long_name(self):
        """Test player with very long name"""
        long_name = "A" * 100
        player = ESPNPlayerData(
            id="12345",
            name=long_name,
            team="TB",
            position="WR"
        )

        assert player.name == long_name

    def test_set_week_points_with_zero(self):
        """Test setting week points to zero"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )

        player.set_week_points(5, 0.0)

        assert player.get_week_points(5) == 0.0

    def test_set_week_points_with_negative(self):
        """Test setting negative week points"""
        player = ESPNPlayerData(
            id="12345",
            name="Bad Week",
            team="TB",
            position="DST"
        )

        player.set_week_points(8, -3.5)

        assert player.get_week_points(8) == -3.5


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_full_season_projection_workflow(self):
        """Test creating and populating a full season projection"""
        player = ESPNPlayerData(
            id="12345",
            name="Star Player",
            team="TB",
            position="QB",
            bye_week=7,
            average_draft_position=1.5,
            fantasy_points=300.0
        )

        # Set projections for all weeks except bye
        for week in range(1, 18):
            if week != 7:  # Skip bye week
                player.set_week_points(week, 20.0)

        all_points = player.get_all_weekly_points()
        non_bye_weeks = [w for w in range(1, 18) if w != 7]

        assert all(all_points[w] == 20.0 for w in non_bye_weeks)
        assert all_points[7] is None  # Bye week

    def test_projection_data_with_multiple_positions(self):
        """Test ProjectionData with players from all positions"""
        players = [
            ESPNPlayerData(id="1", name="QB", team="TB", position="QB"),
            ESPNPlayerData(id="2", name="RB", team="KC", position="RB"),
            ESPNPlayerData(id="3", name="WR", team="BUF", position="WR"),
            ESPNPlayerData(id="4", name="TE", team="KC", position="TE"),
            ESPNPlayerData(id="5", name="K", team="BAL", position="K"),
            ESPNPlayerData(id="6", name="DST", team="SF", position="DST")
        ]

        projection_data = ProjectionData(
            season=2024,
            scoring_format="ppr",
            total_players=6,
            players=players
        )

        positions = [p.position for p in projection_data.players]
        assert "QB" in positions
        assert "RB" in positions
        assert "WR" in positions
        assert "TE" in positions
        assert "K" in positions
        assert "DST" in positions

    def test_updating_player_data_after_creation(self):
        """Test updating player data after initial creation"""
        player = ESPNPlayerData(
            id="12345",
            name="Rookie Player",
            team="TB",
            position="RB",
            drafted_by="",
            fantasy_points=0.0
        )

        # Update as season progresses
        player.drafted_by = "Opponent Team"
        player.fantasy_points = 150.5
        player.set_week_points(1, 15.0)
        player.set_week_points(2, 20.0)

        assert player.drafted_by == "Opponent Team"
        assert player.fantasy_points == 150.5
        assert player.get_week_points(1) == 15.0
        assert player.get_week_points(2) == 20.0


class TestESPNPlayerDataProjectedWeeks:
    """Test projected_weeks dictionary functionality for players_projected.csv export"""

    def test_projected_weeks_default_empty_dict(self):
        """Test that projected_weeks defaults to empty dict"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        assert player.projected_weeks == {}

    def test_set_week_projected_valid_week(self):
        """Test setting projected points for a valid week"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        player.set_week_projected(1, 22.5)
        assert player.projected_weeks[1] == 22.5

    def test_set_week_projected_all_weeks(self):
        """Test setting projected points for all weeks 1-17"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        for week in range(1, 18):
            player.set_week_projected(week, float(week * 5))

        for week in range(1, 18):
            assert player.projected_weeks[week] == float(week * 5)

    def test_set_week_projected_invalid_week_low(self):
        """Test setting projected points for week < 1 is ignored"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        player.set_week_projected(0, 25.5)
        assert 0 not in player.projected_weeks

    def test_set_week_projected_invalid_week_high(self):
        """Test setting projected points for week > 17 is ignored"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        player.set_week_projected(18, 25.5)
        assert 18 not in player.projected_weeks

    def test_get_week_projected_set_value(self):
        """Test getting projected points for a week that was set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        player.set_week_projected(10, 30.2)
        assert player.get_week_projected(10) == 30.2

    def test_get_week_projected_unset_value(self):
        """Test getting projected points for a week that was not set returns None"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        assert player.get_week_projected(5) is None

    def test_get_week_projected_invalid_week_low(self):
        """Test getting projected points for week < 1 returns None"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        assert player.get_week_projected(0) is None

    def test_get_week_projected_invalid_week_high(self):
        """Test getting projected points for week > 17 returns None"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        assert player.get_week_projected(18) is None

    def test_get_all_weekly_projected_no_points_set(self):
        """Test get_all_weekly_projected with no points set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        all_projected = player.get_all_weekly_projected()
        assert len(all_projected) == 17
        assert all(all_projected[w] is None for w in range(1, 18))

    def test_get_all_weekly_projected_some_points_set(self):
        """Test get_all_weekly_projected with some weeks set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        player.set_week_projected(1, 20.0)
        player.set_week_projected(5, 25.0)
        player.set_week_projected(17, 30.0)

        all_projected = player.get_all_weekly_projected()
        assert all_projected[1] == 20.0
        assert all_projected[5] == 25.0
        assert all_projected[17] == 30.0
        assert all_projected[2] is None
        assert all_projected[10] is None

    def test_get_all_weekly_projected_all_points_set(self):
        """Test get_all_weekly_projected with all weeks set"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        for week in range(1, 18):
            player.set_week_projected(week, 20.0)

        all_projected = player.get_all_weekly_projected()
        assert len(all_projected) == 17
        assert all(all_projected[w] == 20.0 for w in range(1, 18))

    def test_projected_independent_of_week_points(self):
        """Test that projected_weeks is independent of week_N_points fields"""
        player = ESPNPlayerData(
            id="12345",
            name="Test Player",
            team="TB",
            position="QB"
        )
        # Set different values for actual and projected
        player.set_week_points(1, 38.76)  # Actual score
        player.set_week_projected(1, 20.83)  # Projected score

        # They should be independent
        assert player.get_week_points(1) == 38.76
        assert player.get_week_projected(1) == 20.83
        assert player.get_week_points(1) != player.get_week_projected(1)
