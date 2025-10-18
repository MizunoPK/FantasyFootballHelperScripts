"""
Unit Tests for NFL Scores Models Module

Tests all Pydantic data models including Team, GameScore, WeeklyScores,
and custom exceptions.

Author: Kai Mizuno
"""

import pytest
from datetime import datetime, timezone
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "nfl-scores-fetcher"))

from nfl_scores_models import (
    Team,
    GameScore,
    WeeklyScores,
    ScoreDataCollectionError,
    GameDataValidationError,
    NFLAPIError
)


# ============================================================================
# TEAM MODEL TESTS
# ============================================================================

class TestTeamModel:
    """Test Team Pydantic model"""

    def test_team_basic_creation(self):
        """Test creating a basic Team with required fields"""
        team = Team(
            id="1",
            name="Cowboys",
            display_name="Dallas Cowboys",
            abbreviation="DAL",
            location="Dallas"
        )

        assert team.id == "1"
        assert team.name == "Cowboys"
        assert team.display_name == "Dallas Cowboys"
        assert team.abbreviation == "DAL"
        assert team.location == "Dallas"

    def test_team_with_optional_fields(self):
        """Test creating Team with all optional fields"""
        team = Team(
            id="1",
            name="Cowboys",
            display_name="Dallas Cowboys",
            abbreviation="DAL",
            location="Dallas",
            color="#003594",
            alternate_color="#041E42",
            logo_url="https://example.com/logo.png",
            record="8-2",
            score=24
        )

        assert team.color == "#003594"
        assert team.alternate_color == "#041E42"
        assert team.logo_url == "https://example.com/logo.png"
        assert team.record == "8-2"
        assert team.score == 24

    def test_team_optional_fields_default_to_none(self):
        """Test that optional fields default to None"""
        team = Team(
            id="1",
            name="Cowboys",
            display_name="Dallas Cowboys",
            abbreviation="DAL",
            location="Dallas"
        )

        assert team.color is None
        assert team.alternate_color is None
        assert team.logo_url is None
        assert team.record is None
        assert team.score is None


# ============================================================================
# GAMESCORE MODEL TESTS
# ============================================================================

class TestGameScoreModel:
    """Test GameScore Pydantic model"""

    @pytest.fixture
    def sample_teams(self):
        """Create sample home and away teams"""
        home_team = Team(
            id="1",
            name="Cowboys",
            display_name="Dallas Cowboys",
            abbreviation="DAL",
            location="Dallas"
        )
        away_team = Team(
            id="2",
            name="Giants",
            display_name="New York Giants",
            abbreviation="NYG",
            location="New York"
        )
        return home_team, away_team

    def test_gamescore_basic_creation(self, sample_teams):
        """Test creating a basic GameScore with required fields"""
        home_team, away_team = sample_teams

        game = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=24,
            away_score=17,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True
        )

        assert game.game_id == "401547416"
        assert game.week == 5
        assert game.season == 2025
        assert game.home_score == 24
        assert game.away_score == 17
        assert game.is_completed == True

    def test_gamescore_derived_fields_calculated(self, sample_teams):
        """Test that derived fields are automatically calculated"""
        home_team, away_team = sample_teams

        game = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=24,
            away_score=17,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True
        )

        # Check derived fields
        assert game.total_points == 41  # 24 + 17
        assert game.point_difference == 7  # abs(24 - 17)
        assert game.winning_team == "DAL"  # Home team won

    def test_gamescore_away_team_wins(self, sample_teams):
        """Test derived fields when away team wins"""
        home_team, away_team = sample_teams

        game = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=14,
            away_score=21,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True
        )

        assert game.total_points == 35
        assert game.point_difference == 7
        assert game.winning_team == "NYG"  # Away team won

    def test_gamescore_tie_game(self, sample_teams):
        """Test derived fields for a tie game"""
        home_team, away_team = sample_teams

        game = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=17,
            away_score=17,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True
        )

        assert game.total_points == 34
        assert game.point_difference == 0
        assert game.winning_team == "TIE"

    def test_gamescore_overtime_detection(self, sample_teams):
        """Test overtime detection from quarter scores"""
        home_team, away_team = sample_teams

        # Game with overtime
        game_ot = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=27,
            away_score=24,
            status="STATUS_FINAL",
            status_detail="Final/OT",
            is_completed=True,
            home_score_q1=7,
            home_score_q2=7,
            home_score_q3=7,
            home_score_q4=3,
            home_score_ot=3,
            away_score_q1=7,
            away_score_q2=7,
            away_score_q3=7,
            away_score_q4=3,
            away_score_ot=0
        )

        assert game_ot.is_overtime == True

        # Game without overtime
        game_no_ot = GameScore(
            game_id="401547417",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=24,
            away_score=17,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True,
            home_score_ot=None,
            away_score_ot=None
        )

        assert game_no_ot.is_overtime == False

    def test_gamescore_with_venue_information(self, sample_teams):
        """Test GameScore with complete venue information"""
        home_team, away_team = sample_teams

        game = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=24,
            away_score=17,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True,
            venue_name="AT&T Stadium",
            venue_city="Arlington",
            venue_state="TX",
            venue_capacity=80000,
            attendance=75432
        )

        assert game.venue_name == "AT&T Stadium"
        assert game.venue_city == "Arlington"
        assert game.venue_state == "TX"
        assert game.venue_capacity == 80000
        assert game.attendance == 75432

    def test_gamescore_with_weather(self, sample_teams):
        """Test GameScore with weather information"""
        home_team, away_team = sample_teams

        game = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=24,
            away_score=17,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True,
            temperature=72,
            weather_description="Clear",
            wind_speed=8
        )

        assert game.temperature == 72
        assert game.weather_description == "Clear"
        assert game.wind_speed == 8

    def test_gamescore_with_betting_odds(self, sample_teams):
        """Test GameScore with betting information"""
        home_team, away_team = sample_teams

        game = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=24,
            away_score=17,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True,
            home_team_odds=-7.5,
            away_team_odds=7.5,
            over_under=45.5
        )

        assert game.home_team_odds == -7.5
        assert game.away_team_odds == 7.5
        assert game.over_under == 45.5

    def test_gamescore_with_statistics(self, sample_teams):
        """Test GameScore with game statistics"""
        home_team, away_team = sample_teams

        game = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=24,
            away_score=17,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True,
            home_total_yards=385,
            away_total_yards=312,
            home_turnovers=1,
            away_turnovers=2
        )

        assert game.home_total_yards == 385
        assert game.away_total_yards == 312
        assert game.home_turnovers == 1
        assert game.away_turnovers == 2

    def test_gamescore_updated_at_timestamp(self, sample_teams):
        """Test that updated_at timestamp is automatically set"""
        home_team, away_team = sample_teams

        game = GameScore(
            game_id="401547416",
            date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=24,
            away_score=17,
            status="STATUS_FINAL",
            status_detail="Final",
            is_completed=True
        )

        assert game.updated_at is not None
        assert isinstance(game.updated_at, datetime)


# ============================================================================
# WEEKLYSCORES MODEL TESTS
# ============================================================================

class TestWeeklyScoresModel:
    """Test WeeklyScores container model"""

    @pytest.fixture
    def sample_games(self):
        """Create list of sample games"""
        home_team = Team(
            id="1", name="Cowboys", display_name="Dallas Cowboys",
            abbreviation="DAL", location="Dallas"
        )
        away_team = Team(
            id="2", name="Giants", display_name="New York Giants",
            abbreviation="NYG", location="New York"
        )

        games = []
        for i in range(3):
            game = GameScore(
                game_id=f"40154741{i}",
                date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
                week=5,
                season=2025,
                season_type=2,
                home_team=home_team,
                away_team=away_team,
                home_score=24,
                away_score=17,
                status="STATUS_FINAL",
                status_detail="Final",
                is_completed=True
            )
            games.append(game)
        return games

    def test_weeklyscores_creation(self, sample_games):
        """Test creating WeeklyScores container"""
        weekly = WeeklyScores(
            week=5,
            season=2025,
            season_type=2,
            total_games=3,
            completed_games=3,
            games=sample_games
        )

        assert weekly.week == 5
        assert weekly.season == 2025
        assert weekly.total_games == 3
        assert weekly.completed_games == 3
        assert len(weekly.games) == 3

    def test_weeklyscores_generated_at_timestamp(self, sample_games):
        """Test that generated_at timestamp is automatically set"""
        weekly = WeeklyScores(
            week=5,
            season=2025,
            season_type=2,
            total_games=3,
            completed_games=3,
            games=sample_games
        )

        assert weekly.generated_at is not None
        assert isinstance(weekly.generated_at, datetime)

    def test_weeklyscores_empty_games_list(self):
        """Test WeeklyScores with empty games list"""
        weekly = WeeklyScores(
            week=5,
            season=2025,
            season_type=2,
            total_games=0,
            completed_games=0,
            games=[]
        )

        assert weekly.total_games == 0
        assert len(weekly.games) == 0


# ============================================================================
# CUSTOM EXCEPTIONS TESTS
# ============================================================================

class TestCustomExceptions:
    """Test custom exception classes"""

    def test_score_data_collection_error(self):
        """Test ScoreDataCollectionError can be raised"""
        with pytest.raises(ScoreDataCollectionError) as exc_info:
            raise ScoreDataCollectionError("Collection failed")

        assert "Collection failed" in str(exc_info.value)

    def test_game_data_validation_error(self):
        """Test GameDataValidationError can be raised"""
        with pytest.raises(GameDataValidationError) as exc_info:
            raise GameDataValidationError("Validation failed")

        assert "Validation failed" in str(exc_info.value)

    def test_nfl_api_error(self):
        """Test NFLAPIError can be raised"""
        with pytest.raises(NFLAPIError) as exc_info:
            raise NFLAPIError("API request failed")

        assert "API request failed" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
