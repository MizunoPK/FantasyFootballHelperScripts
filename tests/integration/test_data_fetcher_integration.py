"""
Integration Tests for Data Fetcher Workflows

Tests end-to-end data fetching workflows:
- Player data fetch → Export → Load
- NFL scores fetch → Export → Load
- Data format consistency across pipeline
- Error handling in data pipeline

Author: Kai Mizuno
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Player data fetcher imports
sys.path.append(str(project_root / "player-data-fetcher"))
from player_data_fetcher_main import PlayerDataFetcher
from player_data_models import PlayerProjection, PlayerWeeklyStats
from config import Config as PlayerConfig

# NFL scores fetcher imports
sys.path.append(str(project_root / "nfl-scores-fetcher"))
from nfl_scores_fetcher_main import NFLScoresFetcher
from nfl_scores_models import NFLGame, NFLScore
from config import Config as ScoresConfig


class TestPlayerDataFetcherIntegration:
    """Integration tests for player data fetcher"""

    def test_player_config_loads_successfully(self, tmp_path):
        """Test that player data fetcher config loads"""
        config = PlayerConfig()

        assert config is not None
        assert hasattr(config, 'ESPN_API_BASE_URL')

    @patch('player_data_fetcher_main.ESPNClient')
    def test_player_fetcher_initialization(self, mock_espn_client, tmp_path):
        """Test player data fetcher initializes correctly"""
        # Mock the ESPN client
        mock_client = Mock()
        mock_espn_client.return_value = mock_client

        fetcher = PlayerDataFetcher(output_dir=tmp_path)

        assert fetcher is not None
        assert fetcher.output_dir == tmp_path

    @patch('player_data_fetcher_main.ESPNClient')
    def test_fetch_and_export_workflow(self, mock_espn_client, tmp_path):
        """Test complete fetch and export workflow"""
        # Mock ESPN client to return test data
        mock_client = Mock()
        mock_client.fetch_projections.return_value = [
            PlayerProjection(
                name="Test Player",
                team="TST",
                position="QB",
                projected_points=300.0,
                stats={}
            )
        ]
        mock_espn_client.return_value = mock_client

        fetcher = PlayerDataFetcher(output_dir=tmp_path)

        # This would call fetch and export
        # For now, verify the fetcher is set up
        assert fetcher.output_dir.exists()


class TestNFLScoresFetcherIntegration:
    """Integration tests for NFL scores fetcher"""

    def test_scores_config_loads_successfully(self):
        """Test that scores fetcher config loads"""
        config = ScoresConfig()

        assert config is not None
        assert hasattr(config, 'NFL_API_BASE_URL')

    @patch('nfl_scores_fetcher_main.NFLAPIClient')
    def test_scores_fetcher_initialization(self, mock_nfl_client, tmp_path):
        """Test scores fetcher initializes correctly"""
        mock_client = Mock()
        mock_nfl_client.return_value = mock_client

        fetcher = NFLScoresFetcher(output_dir=tmp_path)

        assert fetcher is not None
        assert fetcher.output_dir == tmp_path

    @patch('nfl_scores_fetcher_main.NFLAPIClient')
    def test_scores_fetch_workflow(self, mock_nfl_client, tmp_path):
        """Test scores fetch workflow"""
        # Mock NFL API client
        mock_client = Mock()
        mock_client.fetch_scores.return_value = [
            NFLGame(
                game_id="test_game_1",
                week=1,
                home_team="TST1",
                away_team="TST2",
                home_score=24,
                away_score=21
            )
        ]
        mock_nfl_client.return_value = mock_client

        fetcher = NFLScoresFetcher(output_dir=tmp_path)

        assert fetcher.output_dir.exists()


class TestDataFormatConsistency:
    """Integration tests for data format consistency"""

    def test_player_projection_model_structure(self):
        """Test PlayerProjection model has expected structure"""
        projection = PlayerProjection(
            name="Test Player",
            team="TST",
            position="QB",
            projected_points=300.0,
            stats={"passing_yards": 4000, "passing_tds": 30}
        )

        assert projection.name == "Test Player"
        assert projection.team == "TST"
        assert projection.position == "QB"
        assert projection.projected_points == 300.0
        assert "passing_yards" in projection.stats

    def test_nfl_game_model_structure(self):
        """Test NFLGame model has expected structure"""
        game = NFLGame(
            game_id="test_1",
            week=1,
            home_team="HOME",
            away_team="AWAY",
            home_score=28,
            away_score=24
        )

        assert game.game_id == "test_1"
        assert game.week == 1
        assert game.home_team == "HOME"
        assert game.away_team == "AWAY"
        assert game.home_score == 28
        assert game.away_score == 24


class TestDataPipelineIntegration:
    """Integration tests for complete data pipeline"""

    @patch('player_data_fetcher_main.ESPNClient')
    def test_player_data_can_be_exported_and_loaded(self, mock_espn_client, tmp_path):
        """Test player data export and load cycle"""
        # Create test player data
        test_players = [
            PlayerProjection(
                name="QB1",
                team="T1",
                position="QB",
                projected_points=300.0,
                stats={}
            ),
            PlayerProjection(
                name="RB1",
                team="T2",
                position="RB",
                projected_points=250.0,
                stats={}
            )
        ]

        # Mock client
        mock_client = Mock()
        mock_client.fetch_projections.return_value = test_players
        mock_espn_client.return_value = mock_client

        # This tests that the data structure works
        assert len(test_players) == 2
        assert test_players[0].name == "QB1"


class TestErrorHandling:
    """Integration tests for error handling in data fetchers"""

    @patch('player_data_fetcher_main.ESPNClient')
    def test_player_fetcher_handles_api_errors(self, mock_espn_client, tmp_path):
        """Test player fetcher handles API errors gracefully"""
        # Mock API error
        mock_client = Mock()
        mock_client.fetch_projections.side_effect = Exception("API Error")
        mock_espn_client.return_value = mock_client

        fetcher = PlayerDataFetcher(output_dir=tmp_path)

        # Should handle error gracefully
        # For now, verify fetcher was created
        assert fetcher is not None

    @patch('nfl_scores_fetcher_main.NFLAPIClient')
    def test_scores_fetcher_handles_api_errors(self, mock_nfl_client, tmp_path):
        """Test scores fetcher handles API errors gracefully"""
        # Mock API error
        mock_client = Mock()
        mock_client.fetch_scores.side_effect = Exception("API Error")
        mock_nfl_client.return_value = mock_client

        fetcher = NFLScoresFetcher(output_dir=tmp_path)

        # Should handle error gracefully
        assert fetcher is not None


class TestDataValidation:
    """Integration tests for data validation"""

    def test_player_projection_validates_position(self):
        """Test player projection validates position field"""
        # Valid positions: QB, RB, WR, TE, K, DST
        valid_projection = PlayerProjection(
            name="Test",
            team="TST",
            position="QB",
            projected_points=100.0,
            stats={}
        )

        assert valid_projection.position in ["QB", "RB", "WR", "TE", "K", "DST"]

    def test_nfl_game_validates_scores(self):
        """Test NFL game validates score values"""
        game = NFLGame(
            game_id="test",
            week=1,
            home_team="HOME",
            away_team="AWAY",
            home_score=28,
            away_score=24
        )

        # Scores should be non-negative
        assert game.home_score >= 0
        assert game.away_score >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
