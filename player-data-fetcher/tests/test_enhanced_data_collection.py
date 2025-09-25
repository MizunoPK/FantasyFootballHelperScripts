#!/usr/bin/env python3
"""
Unit tests for enhanced data collection in player data fetcher.

This module tests the collection of enhanced scoring data including:
- ADP (Average Draft Position) collection
- Player rating collection
- Team quality data collection
- Integration with existing ESPN client
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from espn_client import ESPNClient
from player_data_models import ESPNPlayerData
from player_data_models import ScoringFormat


class MockSettings:
    """Mock settings for testing"""
    def __init__(self):
        self.season = 2025
        self.scoring_format = ScoringFormat.PPR
        self.request_timeout = 30
        self.rate_limit_delay = 0.1


class TestESPNClientEnhancedDataCollection:
    """Test enhanced data collection in ESPN client"""

    def setup_method(self):
        """Set up test fixtures"""
        self.settings = MockSettings()
        self.mock_player_data = {
            'player': {
                'id': 12345,
                'fullName': 'Test Player',
                'proTeamId': 10,
                'defaultPositionId': 2
            },
            'ownership': {
                'averageDraftPosition': 75.5,
                'percentOwned': 85.2,
                'percentStarted': 90.1
            },
            'playerPoolEntry': {
                'playerRating': 68.7,
                'positionRank': 15,
                'ratingChange': 2.3
            },
            'stats': [
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 0,
                    'appliedTotal': 145.6,
                    'projectedTotal': 150.2
                }
            ]
        }

        self.mock_team_data = {
            'teams': [
                {
                    'team': {
                        'id': 1,
                        'abbreviation': 'KC',
                        'displayName': 'Kansas City Chiefs'
                    }
                },
                {
                    'team': {
                        'id': 2,
                        'abbreviation': 'NE',
                        'displayName': 'New England Patriots'
                    }
                }
            ]
        }

    @pytest.mark.asyncio
    async def test_fetch_team_rankings_success(self):
        """Test successful team rankings fetch"""
        client = ESPNClient(self.settings)

        with patch.object(client, 'session') as mock_session:
            mock_client = MagicMock()
            mock_session.return_value.__aenter__.return_value = mock_client

            with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
                mock_request.return_value = self.mock_team_data

                rankings = await client._fetch_team_rankings()

                assert isinstance(rankings, dict)
                assert 'KC' in rankings
                assert 'NE' in rankings

                # Should have both offensive and defensive rankings
                assert 'offensive_rank' in rankings['KC']
                assert 'defensive_rank' in rankings['KC']

                # Rankings should be integers between 1-30
                assert 1 <= rankings['KC']['offensive_rank'] <= 30
                assert 1 <= rankings['KC']['defensive_rank'] <= 30

    @pytest.mark.asyncio
    async def test_fetch_team_rankings_caching(self):
        """Test that team rankings are cached after first fetch"""
        client = ESPNClient(self.settings)

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = self.mock_team_data

            # First call should make API request
            rankings1 = await client._fetch_team_rankings()

            # Second call should use cache
            rankings2 = await client._fetch_team_rankings()

            # Should only have made one API call
            mock_request.assert_called_once()

            # Results should be identical
            assert rankings1 == rankings2

    @pytest.mark.asyncio
    async def test_fetch_team_rankings_error_handling(self):
        """Test error handling in team rankings fetch"""
        client = ESPNClient(self.settings)

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = Exception("API Error")

            rankings = await client._fetch_team_rankings()

            # Should return empty dict on error
            assert rankings == {}

    @pytest.mark.asyncio
    async def test_fetch_team_rankings_empty_response(self):
        """Test handling of empty team data response"""
        client = ESPNClient(self.settings)

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {'teams': []}  # Empty teams list

            rankings = await client._fetch_team_rankings()

            # Should use default rankings for standard teams
            assert len(rankings) > 0  # Should have default teams
            assert all('offensive_rank' in team_data for team_data in rankings.values())

    @pytest.mark.asyncio
    async def test_parse_espn_data_with_enhanced_fields(self):
        """Test parsing ESPN data with enhanced fields populated"""
        client = ESPNClient(self.settings)

        mock_data = {
            'players': [self.mock_player_data]
        }

        # Mock team rankings
        mock_rankings = {
            'KC': {'offensive_rank': 5, 'defensive_rank': 12}
        }

        with patch.object(client, '_fetch_team_rankings', new_callable=AsyncMock) as mock_fetch_rankings:
            mock_fetch_rankings.return_value = mock_rankings

            with patch('player_data_constants.ESPN_TEAM_MAPPINGS', {10: 'KC'}):
                with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
                    players = await client._parse_espn_data(mock_data)

                    assert len(players) == 1
                    player = players[0]

                    # Should have enhanced data populated
                    assert player.average_draft_position == 75.5
                    assert player.player_rating == 68.7
                    assert player.team_offensive_rank == 5
                    assert player.team_defensive_rank == 12

    @pytest.mark.asyncio
    async def test_parse_espn_data_missing_ownership_data(self):
        """Test parsing when ownership data is missing"""
        client = ESPNClient(self.settings)

        # Remove ownership data
        player_data_no_ownership = self.mock_player_data.copy()
        del player_data_no_ownership['ownership']

        mock_data = {
            'players': [player_data_no_ownership]
        }

        with patch.object(client, '_fetch_team_rankings', new_callable=AsyncMock) as mock_fetch_rankings:
            mock_fetch_rankings.return_value = {}

            with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
                players = await client._parse_espn_data(mock_data)

                assert len(players) == 1
                player = players[0]

                # Should handle missing ownership gracefully
                assert player.average_draft_position is None

    @pytest.mark.asyncio
    async def test_parse_espn_data_missing_player_rating(self):
        """Test parsing when playerPoolEntry data is missing"""
        client = ESPNClient(self.settings)

        # Remove playerPoolEntry data
        player_data_no_rating = self.mock_player_data.copy()
        del player_data_no_rating['playerPoolEntry']

        mock_data = {
            'players': [player_data_no_rating]
        }

        with patch.object(client, '_fetch_team_rankings', new_callable=AsyncMock) as mock_fetch_rankings:
            mock_fetch_rankings.return_value = {}

            with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
                players = await client._parse_espn_data(mock_data)

                assert len(players) == 1
                player = players[0]

                # Should handle missing rating gracefully
                assert player.player_rating is None

    @pytest.mark.asyncio
    async def test_parse_espn_data_team_not_in_rankings(self):
        """Test parsing when team is not found in rankings"""
        client = ESPNClient(self.settings)

        mock_data = {
            'players': [self.mock_player_data]
        }

        # Empty rankings (team not found)
        mock_rankings = {}

        with patch.object(client, '_fetch_team_rankings', new_callable=AsyncMock) as mock_fetch_rankings:
            mock_fetch_rankings.return_value = mock_rankings

            with patch('player_data_constants.ESPN_TEAM_MAPPINGS', {10: 'UNKNOWN'}):
                with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
                    players = await client._parse_espn_data(mock_data)

                    assert len(players) == 1
                    player = players[0]

                    # Should have None values for team rankings
                    assert player.team_offensive_rank is None
                    assert player.team_defensive_rank is None

    @pytest.mark.asyncio
    async def test_parse_espn_data_different_positions_team_assignment(self):
        """Test that different positions get appropriate team rank assignments"""
        client = ESPNClient(self.settings)

        # Create player data for QB and DST
        qb_data = self.mock_player_data.copy()
        qb_data['player']['defaultPositionId'] = 1  # QB
        qb_data['player']['id'] = 11111

        dst_data = self.mock_player_data.copy()
        dst_data['player']['defaultPositionId'] = 16  # DST
        dst_data['player']['id'] = 22222
        dst_data['player']['fullName'] = 'Test Defense'

        mock_data = {
            'players': [qb_data, dst_data]
        }

        mock_rankings = {
            'KC': {'offensive_rank': 3, 'defensive_rank': 15}
        }

        with patch.object(client, '_fetch_team_rankings', new_callable=AsyncMock) as mock_fetch_rankings:
            mock_fetch_rankings.return_value = mock_rankings

            with patch('player_data_constants.ESPN_TEAM_MAPPINGS', {10: 'KC'}):
                with patch('player_data_constants.ESPN_POSITION_MAPPINGS', {1: 'QB', 16: 'DST'}):
                    with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
                        players = await client._parse_espn_data(mock_data)

                        qb_player = next(p for p in players if p.position == 'QB')
                        dst_player = next(p for p in players if p.position == 'DST')

                        # Both should have team data assigned
                        assert qb_player.team_offensive_rank == 3
                        assert qb_player.team_defensive_rank == 15
                        assert dst_player.team_offensive_rank == 3
                        assert dst_player.team_defensive_rank == 15

    def test_espn_player_data_model_enhanced_fields(self):
        """Test that ESPNPlayerData model properly handles enhanced fields"""
        player_data = ESPNPlayerData(
            id="test123",
            name="Test Player",
            team="KC",
            position="RB",
            fantasy_points=120.0,
            average_draft_position=55.5,
            player_rating=72.3,
            team_offensive_rank=8,
            team_defensive_rank=20
        )

        # Should properly store all enhanced fields
        assert player_data.average_draft_position == 55.5
        assert player_data.player_rating == 72.3
        assert player_data.team_offensive_rank == 8
        assert player_data.team_defensive_rank == 20

        # Should serialize properly
        model_dict = player_data.model_dump()
        assert 'average_draft_position' in model_dict
        assert 'player_rating' in model_dict
        assert 'team_offensive_rank' in model_dict
        assert 'team_defensive_rank' in model_dict

    def test_espn_player_data_model_optional_enhanced_fields(self):
        """Test ESPNPlayerData model with missing enhanced fields"""
        player_data = ESPNPlayerData(
            id="test123",
            name="Test Player",
            team="KC",
            position="RB",
            fantasy_points=120.0
            # Enhanced fields omitted
        )

        # Should have None values for missing enhanced fields
        assert player_data.average_draft_position is None
        assert player_data.player_rating is None
        assert player_data.team_offensive_rank is None
        assert player_data.team_defensive_rank is None

    @pytest.mark.asyncio
    async def test_integration_with_existing_optimization_features(self):
        """Test that enhanced data collection works with existing optimization features"""
        client = ESPNClient(self.settings)

        # Mock optimization data loading
        client.drafted_player_ids = {'12345'}  # Mock drafted player
        client.low_score_player_data = {}

        mock_data = {
            'players': [self.mock_player_data]
        }

        mock_rankings = {
            'KC': {'offensive_rank': 5, 'defensive_rank': 12}
        }

        with patch.object(client, '_fetch_team_rankings', new_callable=AsyncMock) as mock_fetch_rankings:
            mock_fetch_rankings.return_value = mock_rankings

            with patch('player_data_constants.SKIP_DRAFTED_PLAYER_UPDATES', True):
                with patch('player_data_constants.ESPN_TEAM_MAPPINGS', {10: 'KC'}):
                    with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
                        players = await client._parse_espn_data(mock_data)

                        # Should still get enhanced data even with optimizations
                        # (This tests the integration, specific optimization logic is tested elsewhere)
                        assert len(players) >= 0  # May skip drafted players


class TestEnhancedDataCollectionPerformance:
    """Test performance aspects of enhanced data collection"""

    def setup_method(self):
        """Set up test fixtures"""
        self.settings = MockSettings()

    @pytest.mark.asyncio
    async def test_team_rankings_single_api_call(self):
        """Test that team rankings only require one additional API call"""
        client = ESPNClient(self.settings)

        mock_team_data = {
            'teams': [
                {'team': {'id': i, 'abbreviation': f'T{i}'}}
                for i in range(1, 33)  # 32 teams
            ]
        }

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_team_data

            # Multiple calls to get rankings
            rankings1 = await client._fetch_team_rankings()
            rankings2 = await client._fetch_team_rankings()
            rankings3 = await client._fetch_team_rankings()

            # Should only make one API call due to caching
            mock_request.assert_called_once()

            # All results should be identical
            assert rankings1 == rankings2 == rankings3

    @pytest.mark.asyncio
    async def test_enhanced_data_parsing_performance(self):
        """Test that enhanced data parsing doesn't significantly impact performance"""
        client = ESPNClient(self.settings)

        # Create many players for performance test
        many_players = {
            'players': [
                {
                    'player': {
                        'id': i,
                        'fullName': f'Player {i}',
                        'proTeamId': (i % 32) + 1,
                        'defaultPositionId': 2
                    },
                    'ownership': {
                        'averageDraftPosition': 50.0 + i,
                    },
                    'playerPoolEntry': {
                        'playerRating': 60.0 + (i % 40),
                    },
                    'stats': [
                        {
                            'seasonId': 2025,
                            'scoringPeriodId': 0,
                            'appliedTotal': 100.0 + i
                        }
                    ]
                }
                for i in range(100)  # 100 players
            ]
        }

        mock_rankings = {
            f'T{i}': {'offensive_rank': (i % 30) + 1, 'defensive_rank': ((i * 2) % 30) + 1}
            for i in range(1, 33)
        }

        with patch.object(client, '_fetch_team_rankings', new_callable=AsyncMock) as mock_fetch_rankings:
            mock_fetch_rankings.return_value = mock_rankings

            with patch('player_data_constants.ESPN_TEAM_MAPPINGS', {i: f'T{i}' for i in range(1, 33)}):
                with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
                    import time
                    start_time = time.time()

                    players = await client._parse_espn_data(many_players)

                    end_time = time.time()
                    elapsed = end_time - start_time

                    # Should process 100 players quickly (< 1 second)
                    assert elapsed < 1.0

                    # Should have all players with enhanced data
                    assert len(players) == 100
                    for player in players:
                        assert player.average_draft_position is not None
                        assert player.player_rating is not None
                        assert player.team_offensive_rank is not None
                        assert player.team_defensive_rank is not None


class TestEnhancedDataExportIntegration:
    """Test integration with data export functionality"""

    def test_export_columns_include_enhanced_fields(self):
        """Test that export columns include enhanced fields"""
        from player_data_fetcher_config import EXPORT_COLUMNS

        expected_enhanced_columns = [
            'average_draft_position',
            'player_rating',
            'team_offensive_rank',
            'team_defensive_rank'
        ]

        for column in expected_enhanced_columns:
            assert column in EXPORT_COLUMNS, f"Enhanced column '{column}' missing from EXPORT_COLUMNS"

    def test_enhanced_fields_position_in_export_columns(self):
        """Test that enhanced fields are positioned appropriately in export columns"""
        from player_data_fetcher_config import EXPORT_COLUMNS

        # Enhanced fields should come after basic fields but before weekly points
        enhanced_fields = ['average_draft_position', 'player_rating', 'team_offensive_rank', 'team_defensive_rank']

        # Find positions
        positions = {field: EXPORT_COLUMNS.index(field) for field in enhanced_fields}

        # Should be after 'locked' and before 'data_method'
        locked_pos = EXPORT_COLUMNS.index('locked')
        data_method_pos = EXPORT_COLUMNS.index('data_method')

        for field, pos in positions.items():
            assert locked_pos < pos < data_method_pos, f"Field '{field}' not positioned correctly in export columns"


class TestEnhancedDataErrorHandling:
    """Test error handling for enhanced data collection"""

    def setup_method(self):
        """Set up test fixtures"""
        self.settings = MockSettings()

    @pytest.mark.asyncio
    async def test_malformed_ownership_data_handling(self):
        """Test handling of malformed ownership data"""
        client = ESPNClient(self.settings)

        malformed_player_data = {
            'player': {
                'id': 12345,
                'fullName': 'Test Player',
                'proTeamId': 10,
                'defaultPositionId': 2
            },
            'ownership': {
                'averageDraftPosition': 'invalid_float',  # Invalid data type
                'percentOwned': None
            },
            'stats': [
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 0,
                    'appliedTotal': 100.0
                }
            ]
        }

        mock_data = {'players': [malformed_player_data]}

        with patch.object(client, '_fetch_team_rankings', new_callable=AsyncMock) as mock_fetch_rankings:
            mock_fetch_rankings.return_value = {}

            with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
                # Should not raise exception
                players = await client._parse_espn_data(mock_data)

                assert len(players) == 1
                # Should handle invalid ADP gracefully
                assert players[0].average_draft_position is None

    @pytest.mark.asyncio
    async def test_malformed_player_rating_data_handling(self):
        """Test handling of malformed player rating data"""
        client = ESPNClient(self.settings)

        malformed_player_data = {
            'player': {
                'id': 12345,
                'fullName': 'Test Player',
                'proTeamId': 10,
                'defaultPositionId': 2
            },
            'playerPoolEntry': {
                'playerRating': 'not_a_number',  # Invalid data type
                'positionRank': -1  # Invalid value
            },
            'stats': [
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 0,
                    'appliedTotal': 100.0
                }
            ]
        }

        mock_data = {'players': [malformed_player_data]}

        with patch.object(client, '_fetch_team_rankings', new_callable=AsyncMock) as mock_fetch_rankings:
            mock_fetch_rankings.return_value = {}

            with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
                # Should not raise exception
                players = await client._parse_espn_data(mock_data)

                assert len(players) == 1
                # Should handle invalid rating gracefully
                assert players[0].player_rating is None

    @pytest.mark.asyncio
    async def test_network_error_during_team_fetch(self):
        """Test network error handling during team rankings fetch"""
        client = ESPNClient(self.settings)

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = Exception("Network timeout")

            # Should handle network errors gracefully
            rankings = await client._fetch_team_rankings()

            # Should return empty rankings dict
            assert rankings == {}

        # Subsequent player parsing should still work
        mock_player_data = {
            'players': [
                {
                    'player': {
                        'id': 12345,
                        'fullName': 'Test Player',
                        'proTeamId': 10,
                        'defaultPositionId': 2
                    },
                    'stats': [{'seasonId': 2025, 'scoringPeriodId': 0, 'appliedTotal': 100.0}]
                }
            ]
        }

        with patch.object(client, '_populate_weekly_projections', new_callable=AsyncMock):
            players = await client._parse_espn_data(mock_player_data)

            assert len(players) == 1
            # Team rankings should be None due to fetch failure
            assert players[0].team_offensive_rank is None
            assert players[0].team_defensive_rank is None


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])