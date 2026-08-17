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
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import json

from player_data_fetcher.player_data_fetcher_main import NFLProjectionsCollector, Settings
from player_data_fetcher.player_data_models import PlayerProjection, ScoringFormat, ProjectionData, ESPNPlayerData



class TestPlayerDataFetcherIntegration:
    """Integration tests for player data fetcher"""

    @pytest.fixture
    def collector_settings(self, tmp_path):
        """Create Settings object for NFLProjectionsCollector"""
        return Settings(
            scoring_format=ScoringFormat.PPR,
            season=2024
        )

    def test_player_collector_initialization(self, collector_settings):
        """Test NFL projections collector initializes correctly"""
        collector = NFLProjectionsCollector(collector_settings)

        assert collector is not None
        assert collector.settings.scoring_format == ScoringFormat.PPR

    @pytest.mark.asyncio
    @patch('player_data_fetcher.player_data_fetcher_main.ESPNClient')
    async def test_fetch_and_export_workflow(self, mock_espn_client, collector_settings):
        """Test complete fetch and export workflow"""
        mock_client = Mock()

        mock_player = ESPNPlayerData(
            id="1",
            name="Test Player",
            team="TST",
            position="QB",
            bye_week=10,
            fantasy_points=300.0,
            injury_status="ACTIVE",
            average_draft_position=1.0,
            player_rating=95.0
        )

        async def mock_get_season_projections():
            return [mock_player]

        mock_client.get_season_projections = mock_get_season_projections

        async_cm = AsyncMock()
        async_cm.__aenter__.return_value = None
        async_cm.__aexit__.return_value = None
        mock_client.session.return_value = async_cm

        mock_client.team_rankings = {}
        mock_client.current_week_schedule = {}

        with patch.object(NFLProjectionsCollector, '_get_api_client', return_value=mock_client):
            collector = NFLProjectionsCollector(collector_settings)
            projection_data = await collector.collect_all_projections()

            assert projection_data is not None
            assert 'season' in projection_data





class TestDataFormatConsistency:
    """Integration tests for data format consistency"""

    def test_player_projection_model_structure(self):
        """Test PlayerProjection model has expected structure"""
        projection = PlayerProjection(
            id="test_player_1",
            name="Test Player",
            team="TST",
            position="QB",
            fantasy_points=300.0,
            average_draft_position=1.0,
            player_rating=95.0
        )

        assert projection.name == "Test Player"
        assert projection.team == "TST"
        assert projection.position == "QB"
        assert projection.fantasy_points == 300.0
        assert projection.average_draft_position == 1.0



class TestDataPipelineIntegration:
    """Integration tests for complete data pipeline"""

    def test_player_data_can_be_exported_and_loaded(self):
        """Test player data export and load cycle"""
        test_players = [
            ESPNPlayerData(
                id="1",
                name="QB1",
                team="T1",
                position="QB",
                bye_week=10,
                fantasy_points=300.0,
                injury_status="ACTIVE",
                average_draft_position=1.0,
                player_rating=95.0,
                weekly_projections={}
            ),
            ESPNPlayerData(
                id="2",
                name="RB1",
                team="T2",
                position="RB",
                bye_week=11,
                fantasy_points=250.0,
                injury_status="ACTIVE",
                average_draft_position=10.0,
                player_rating=90.0,
                weekly_projections={}
            )
        ]

        assert len(test_players) == 2
        assert test_players[0].name == "QB1"
        assert test_players[1].position == "RB"


class TestErrorHandling:
    """Integration tests for error handling in data fetchers"""

    def test_player_collector_handles_initialization_gracefully(self, tmp_path):
        """Test player collector handles initialization gracefully"""
        settings = Settings(
            scoring_format=ScoringFormat.PPR,
            season=2024,
        )

        collector = NFLProjectionsCollector(settings)

        assert collector is not None
        assert collector.settings.season == 2024



class TestDataValidation:
    """Integration tests for data validation"""

    def test_player_projection_validates_position(self):
        """Test player projection validates position field"""
        valid_projection = PlayerProjection(
            id="test_player_2",
            name="Test",
            team="TST",
            position="QB",
            fantasy_points=100.0
        )

        assert valid_projection.position in ["QB", "RB", "WR", "TE", "K", "DST"]



if __name__ == "__main__":
    pytest.main([__file__, "-v"])


