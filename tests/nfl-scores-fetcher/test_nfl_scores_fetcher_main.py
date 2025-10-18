"""
Unit Tests for NFL Scores Fetcher Main Module

Tests the main orchestration module including Settings validation,
NFLScoresCollector class, and main() function.

Author: Kai Mizuno
"""

import pytest
import asyncio
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from pathlib import Path
from datetime import datetime, timezone
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "nfl-scores-fetcher"))

from nfl_scores_fetcher_main import Settings, NFLScoresCollector, main
from nfl_scores_models import GameScore, WeeklyScores, Team


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_game():
    """Create a mock GameScore for testing"""
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

    return GameScore(
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


@pytest.fixture
def mock_games(mock_game):
    """Create list of mock games for testing"""
    games = [mock_game]
    # Add a second game
    home_team2 = Team(id="3", name="Eagles", display_name="Philadelphia Eagles",
                     abbreviation="PHI", location="Philadelphia")
    away_team2 = Team(id="4", name="Washington", display_name="Washington Commanders",
                     abbreviation="WAS", location="Washington")

    game2 = GameScore(
        game_id="401547417",
        date=datetime(2025, 9, 15, 16, 25, tzinfo=timezone.utc),
        week=5,
        season=2025,
        season_type=2,
        home_team=home_team2,
        away_team=away_team2,
        home_score=31,
        away_score=14,
        status="STATUS_FINAL",
        status_detail="Final",
        is_completed=True
    )
    games.append(game2)
    return games


@pytest.fixture
def default_settings():
    """Create default Settings object"""
    return Settings()


@pytest.fixture
def collector(default_settings, tmp_path):
    """Create NFLScoresCollector with temp directory"""
    settings = default_settings
    settings.output_directory = str(tmp_path / "data")
    return NFLScoresCollector(settings)


# ============================================================================
# SETTINGS CLASS TESTS
# ============================================================================

class TestSettings:
    """Test Settings configuration class"""

    def test_settings_default_values(self, default_settings):
        """Test that Settings loads default values from config.py"""
        assert default_settings.season == 2025
        assert default_settings.current_week == 5
        assert default_settings.season_type == 2
        assert default_settings.only_completed_games == False
        assert default_settings.create_csv == True
        assert default_settings.create_excel == True
        assert default_settings.request_timeout == 30

    def test_settings_validation_future_season(self, capsys):
        """Test validation warns about future seasons"""
        settings = Settings(season=2030)
        settings.validate_settings()
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "future" in captured.out.lower()

    def test_settings_validation_old_season(self, capsys):
        """Test validation warns about very old seasons"""
        settings = Settings(season=2020)
        settings.validate_settings()
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "old" in captured.out.lower()

    def test_settings_validation_low_timeout(self, capsys):
        """Test validation warns about low timeout"""
        settings = Settings(request_timeout=5)
        settings.validate_settings()
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "timeout" in captured.out.lower()

    def test_settings_validation_aggressive_rate_limit(self, capsys):
        """Test validation warns about aggressive rate limiting"""
        settings = Settings(rate_limit_delay=0.01)
        settings.validate_settings()
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "rate limit" in captured.out.lower()


# ============================================================================
# NFLSCORESCOLLECTOR CLASS TESTS
# ============================================================================

class TestNFLScoresCollector:
    """Test NFLScoresCollector class"""

    def test_collector_initialization(self, collector):
        """Test collector initializes correctly"""
        assert collector.settings is not None
        assert collector.logger is not None
        assert collector.exporter is not None
        assert isinstance(collector.script_dir, Path)

    @pytest.mark.asyncio
    async def test_collect_scores_specific_week(self, collector, mock_games):
        """Test collecting scores for a specific week"""
        collector.settings.current_week = 5

        with patch('nfl_scores_fetcher_main.NFLAPIClient') as MockClient:
            mock_client = MockClient.return_value
            mock_client.session = MagicMock()
            mock_client.session.return_value.__aenter__ = AsyncMock()
            mock_client.session.return_value.__aexit__ = AsyncMock()
            mock_client.get_week_scores = AsyncMock(return_value=mock_games)

            games = await collector.collect_scores()

            assert len(games) == 2
            assert games[0].week == 5
            mock_client.get_week_scores.assert_called_once_with(week=5)

    @pytest.mark.asyncio
    async def test_collect_scores_recent_games(self, collector, mock_games):
        """Test collecting recent games when no week specified"""
        collector.settings.current_week = None

        with patch('nfl_scores_fetcher_main.NFLAPIClient') as MockClient:
            mock_client = MockClient.return_value
            mock_client.session = MagicMock()
            mock_client.session.return_value.__aenter__ = AsyncMock()
            mock_client.session.return_value.__aexit__ = AsyncMock()
            mock_client.get_completed_games_recent = AsyncMock(return_value=mock_games)

            games = await collector.collect_scores()

            assert len(games) == 2
            mock_client.get_completed_games_recent.assert_called_once_with(days_back=10)

    @pytest.mark.asyncio
    async def test_collect_scores_filter_completed(self, collector, mock_game):
        """Test filtering to only completed games"""
        collector.settings.only_completed_games = True

        # Create mix of completed and in-progress games
        incomplete_game = GameScore(
            game_id="401547418",
            date=datetime(2025, 9, 15, 20, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=mock_game.home_team,
            away_team=mock_game.away_team,
            home_score=14,
            away_score=10,
            status="STATUS_IN_PROGRESS",
            status_detail="3rd Quarter",
            is_completed=False,
            is_in_progress=True
        )
        all_games = [mock_game, incomplete_game]

        with patch('nfl_scores_fetcher_main.NFLAPIClient') as MockClient:
            mock_client = MockClient.return_value
            mock_client.session = MagicMock()
            mock_client.session.return_value.__aenter__ = AsyncMock()
            mock_client.session.return_value.__aexit__ = AsyncMock()
            mock_client.get_week_scores = AsyncMock(return_value=all_games)

            games = await collector.collect_scores()

            assert len(games) == 1
            assert games[0].is_completed == True

    @pytest.mark.asyncio
    async def test_export_data(self, collector, mock_games):
        """Test exporting game data"""
        with patch.object(collector.exporter, 'export_all_formats', new=AsyncMock()) as mock_export:
            mock_export.return_value = ['file1.csv', 'file2.xlsx']

            output_files = await collector.export_data(mock_games)

            assert len(output_files) == 2
            assert 'file1.csv' in output_files
            mock_export.assert_called_once()

            # Verify WeeklyScores object was created
            call_args = mock_export.call_args
            weekly_scores = call_args[0][0]
            assert isinstance(weekly_scores, WeeklyScores)
            assert weekly_scores.week == 5
            assert weekly_scores.total_games == 2
            assert weekly_scores.completed_games == 2

    @pytest.mark.asyncio
    async def test_export_data_empty_games(self, collector):
        """Test exporting with empty games list"""
        with patch.object(collector.exporter, 'export_all_formats', new=AsyncMock()) as mock_export:
            mock_export.return_value = []

            output_files = await collector.export_data([])

            assert len(output_files) == 0

    def test_print_summary_with_games(self, collector, mock_games, capsys):
        """Test printing summary with games"""
        collector.print_summary(mock_games)

        captured = capsys.readouterr()
        assert "SUCCESS" in captured.out
        assert "Total Games: 2" in captured.out
        assert "Completed: 2 games" in captured.out
        assert "DAL" in captured.out or "Cowboys" in captured.out

    def test_print_summary_no_games(self, collector, capsys):
        """Test printing summary with no games"""
        collector.print_summary([])

        captured = capsys.readouterr()
        assert "Total Games: 0" in captured.out
        assert "No games found" in captured.out


# ============================================================================
# MAIN FUNCTION INTEGRATION TESTS
# ============================================================================

class TestMainFunction:
    """Test main() function integration"""

    @pytest.mark.asyncio
    async def test_main_success(self, mock_games):
        """Test successful main() execution"""
        with patch('nfl_scores_fetcher_main.setup_logger') as mock_setup, \
             patch('nfl_scores_fetcher_main.NFLScoresCollector') as MockCollector:

            # Setup mocks
            mock_logger = Mock()
            mock_setup.return_value = mock_logger

            mock_collector = MockCollector.return_value
            mock_collector.collect_scores = AsyncMock(return_value=mock_games)
            mock_collector.export_data = AsyncMock(return_value=['file1.csv'])
            mock_collector.print_summary = Mock()

            # Run main
            await main()

            # Verify calls
            mock_setup.assert_called_once()
            mock_collector.collect_scores.assert_called_once()
            mock_collector.export_data.assert_called_once()
            mock_collector.print_summary.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_no_games_found(self):
        """Test main() when no games are found"""
        with patch('nfl_scores_fetcher_main.setup_logger') as mock_setup, \
             patch('nfl_scores_fetcher_main.NFLScoresCollector') as MockCollector:

            mock_logger = Mock()
            mock_setup.return_value = mock_logger

            mock_collector = MockCollector.return_value
            mock_collector.collect_scores = AsyncMock(return_value=[])

            # Should return early without error
            await main()

            mock_collector.collect_scores.assert_called_once()
            # export_data should not be called when no games
            mock_collector.export_data.assert_not_called()

    @pytest.mark.asyncio
    async def test_main_api_error(self):
        """Test main() handles API errors gracefully"""
        with patch('nfl_scores_fetcher_main.setup_logger') as mock_setup, \
             patch('nfl_scores_fetcher_main.NFLScoresCollector') as MockCollector:

            mock_logger = Mock()
            mock_setup.return_value = mock_logger

            mock_collector = MockCollector.return_value
            mock_collector.collect_scores = AsyncMock(side_effect=Exception("API connection failed"))

            # Should raise exception
            with pytest.raises(Exception) as exc_info:
                await main()

            assert "API" in str(exc_info.value) or "connection" in str(exc_info.value)
            mock_logger.error.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
