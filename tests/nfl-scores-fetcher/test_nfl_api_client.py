"""
Unit Tests for NFL API Client Module

Tests the NFLAPIClient class including HTTP requests, parsing, error handling,
and retry logic.

Author: Kai Mizuno
"""

import pytest
import asyncio
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "nfl-scores-fetcher"))

from nfl_api_client import NFLAPIClient
from nfl_scores_models import GameScore, Team, NFLAPIError
import httpx
from tenacity import RetryError


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_settings():
    """Create mock settings object"""
    settings = Mock()
    settings.season = 2025
    settings.season_type = 2  # Regular season
    settings.current_week = 5
    settings.request_timeout = 30
    settings.rate_limit_delay = 0.1
    settings.only_completed_games = False
    return settings


@pytest.fixture
def api_client(mock_settings):
    """Create NFLAPIClient instance"""
    return NFLAPIClient(mock_settings)


@pytest.fixture
def sample_team_data():
    """Sample team data in ESPN API format"""
    return {
        'id': '1',
        'name': 'Cowboys',
        'displayName': 'Dallas Cowboys',
        'abbreviation': 'DAL',
        'location': 'Dallas',
        'color': '003594',
        'alternateColor': '041E42',
        'logo': 'https://example.com/dal.png',
        'record': {
            'displayValue': '8-2'
        }
    }


@pytest.fixture
def sample_game_event(sample_team_data):
    """Sample game event in ESPN API format"""
    away_team = {
        'id': '2',
        'name': 'Giants',
        'displayName': 'New York Giants',
        'abbreviation': 'NYG',
        'location': 'New York',
        'record': {
            'displayValue': '4-6'
        }
    }

    return {
        'id': '401547416',
        'date': '2025-09-15T13:00:00Z',
        'season': {
            'year': 2025,
            'week': 5,
            'type': 2
        },
        'competitions': [{
            'status': {
                'type': {
                    'name': 'STATUS_FINAL',
                    'detail': 'Final',
                    'completed': True
                }
            },
            'competitors': [
                {
                    'homeAway': 'home',
                    'team': sample_team_data,
                    'score': '24',
                    'linescores': [
                        {'value': 7},
                        {'value': 7},
                        {'value': 3},
                        {'value': 7}
                    ],
                    'statistics': [
                        {'name': 'totalYards', 'displayValue': '385'},
                        {'name': 'turnovers', 'displayValue': '1'}
                    ]
                },
                {
                    'homeAway': 'away',
                    'team': away_team,
                    'score': '17',
                    'linescores': [
                        {'value': 7},
                        {'value': 3},
                        {'value': 0},
                        {'value': 7}
                    ],
                    'statistics': [
                        {'name': 'totalYards', 'displayValue': '312'},
                        {'name': 'turnovers', 'displayValue': '2'}
                    ]
                }
            ],
            'venue': {
                'fullName': "AT&T Stadium",
                'address': {
                    'city': 'Arlington',
                    'state': 'TX'
                },
                'capacity': 80000
            },
            'attendance': 75432,
            'weather': {
                'temperature': 72,
                'conditionId': 'Clear'
            },
            'broadcasts': [
                {'market': {'name': 'FOX'}}
            ]
        }]
    }


@pytest.fixture
def sample_scoreboard_response(sample_game_event):
    """Sample full scoreboard API response"""
    return {
        'events': [sample_game_event]
    }


# ============================================================================
# CLIENT INITIALIZATION TESTS
# ============================================================================

class TestClientInitialization:
    """Test NFLAPIClient initialization"""

    def test_client_initializes_with_settings(self, api_client, mock_settings):
        """Test client initializes correctly with settings"""
        assert api_client.settings == mock_settings
        assert api_client.base_url is not None
        assert api_client.client is None  # Not created until context manager
        assert api_client.logger is not None

    def test_client_has_correct_base_url(self, api_client):
        """Test client has ESPN base URL configured"""
        assert 'espn.com' in api_client.base_url.lower()


# ============================================================================
# CONTEXT MANAGER TESTS
# ============================================================================

class TestSessionContextManager:
    """Test async session context manager"""

    @pytest.mark.asyncio
    async def test_session_creates_client(self, api_client):
        """Test session creates HTTP client"""
        async with api_client.session():
            assert api_client.client is not None
            assert isinstance(api_client.client, httpx.AsyncClient)

    @pytest.mark.asyncio
    async def test_session_closes_client(self, api_client):
        """Test session closes client on exit"""
        async with api_client.session():
            client = api_client.client

        # Client should be closed after context exit
        assert client.is_closed

    @pytest.mark.asyncio
    async def test_session_configures_timeout(self, api_client, mock_settings):
        """Test session configures timeout from settings"""
        async with api_client.session():
            # Timeout should match settings
            assert api_client.client.timeout.read == mock_settings.request_timeout


# ============================================================================
# HTTP REQUEST TESTS
# ============================================================================

class TestMakeRequest:
    """Test _make_request method"""

    @pytest.mark.asyncio
    async def test_make_request_success(self, api_client, sample_scoreboard_response):
        """Test successful HTTP request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_scoreboard_response

        api_client.client = AsyncMock()
        api_client.client.get = AsyncMock(return_value=mock_response)

        result = await api_client._make_request("https://test.com")

        assert result == sample_scoreboard_response
        api_client.client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_make_request_with_params(self, api_client, sample_scoreboard_response):
        """Test HTTP request with query parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_scoreboard_response

        api_client.client = AsyncMock()
        api_client.client.get = AsyncMock(return_value=mock_response)

        params = {'week': 5, 'seasontype': 2}
        await api_client._make_request("https://test.com", params=params)

        api_client.client.get.assert_called_once_with("https://test.com", params=params)

    @pytest.mark.asyncio
    async def test_make_request_rate_limiting_429(self, api_client):
        """Test handling of 429 rate limit response"""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '5'}

        api_client.client = AsyncMock()
        api_client.client.get = AsyncMock(return_value=mock_response)

        # Retry decorator will retry 3 times then raise RetryError
        with pytest.raises(RetryError):
            await api_client._make_request("https://test.com")

    @pytest.mark.asyncio
    async def test_make_request_server_error_500(self, api_client):
        """Test handling of 500 server error"""
        mock_response = Mock()
        mock_response.status_code = 500

        api_client.client = AsyncMock()
        api_client.client.get = AsyncMock(return_value=mock_response)

        # Retry decorator will retry 3 times then raise RetryError
        with pytest.raises(RetryError):
            await api_client._make_request("https://test.com")

    @pytest.mark.asyncio
    async def test_make_request_client_error_404(self, api_client):
        """Test handling of 404 client error"""
        mock_response = Mock()
        mock_response.status_code = 404

        api_client.client = AsyncMock()
        api_client.client.get = AsyncMock(return_value=mock_response)

        # Retry decorator will retry 3 times then raise RetryError
        with pytest.raises(RetryError):
            await api_client._make_request("https://test.com")

    @pytest.mark.asyncio
    async def test_make_request_network_error(self, api_client):
        """Test handling of network errors"""
        api_client.client = AsyncMock()
        api_client.client.get = AsyncMock(side_effect=httpx.RequestError("Connection failed"))

        # Retry decorator will retry 3 times then raise RetryError
        with pytest.raises(RetryError):
            await api_client._make_request("https://test.com")


# ============================================================================
# API ENDPOINT TESTS
# ============================================================================

class TestAPIEndpoints:
    """Test API endpoint methods"""

    @pytest.mark.asyncio
    async def test_get_current_week_scores(self, api_client, sample_scoreboard_response):
        """Test fetching current week scores"""
        with patch.object(api_client, '_make_request', new=AsyncMock(return_value=sample_scoreboard_response)):
            with patch.object(api_client, '_parse_scoreboard_data', return_value=[Mock()]) as mock_parse:
                result = await api_client.get_current_week_scores()

                api_client._make_request.assert_called_once()
                mock_parse.assert_called_once_with(sample_scoreboard_response)
                assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_week_scores(self, api_client, sample_scoreboard_response):
        """Test fetching specific week scores"""
        with patch.object(api_client, '_make_request', new=AsyncMock(return_value=sample_scoreboard_response)):
            with patch.object(api_client, '_parse_scoreboard_data', return_value=[Mock()]) as mock_parse:
                result = await api_client.get_week_scores(week=5)

                # Verify params include week
                call_args = api_client._make_request.call_args
                assert call_args[1]['params']['week'] == 5
                mock_parse.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_completed_games_recent(self, api_client, sample_scoreboard_response):
        """Test fetching recent completed games"""
        mock_completed_game = Mock()
        mock_completed_game.is_completed = True

        mock_incomplete_game = Mock()
        mock_incomplete_game.is_completed = False

        with patch.object(api_client, '_make_request', new=AsyncMock(return_value=sample_scoreboard_response)):
            with patch.object(api_client, '_parse_scoreboard_data', return_value=[mock_completed_game, mock_incomplete_game]):
                result = await api_client.get_completed_games_recent(days_back=7)

                # Should only return completed games
                assert len(result) == 1
                assert result[0].is_completed == True

    @pytest.mark.asyncio
    async def test_get_completed_games_recent_date_range(self, api_client, sample_scoreboard_response):
        """Test recent games uses correct date range"""
        with patch.object(api_client, '_make_request', new=AsyncMock(return_value=sample_scoreboard_response)):
            with patch.object(api_client, '_parse_scoreboard_data', return_value=[]):
                await api_client.get_completed_games_recent(days_back=10)

                # Verify date range in params
                call_args = api_client._make_request.call_args
                params = call_args[1]['params']
                assert 'dates' in params
                assert '-' in params['dates']  # Should be date range format

    @pytest.mark.asyncio
    async def test_get_completed_games_recent_handles_errors(self, api_client):
        """Test recent games handles errors gracefully"""
        with patch.object(api_client, '_make_request', new=AsyncMock(side_effect=Exception("API error"))):
            result = await api_client.get_completed_games_recent(days_back=7)

            # Should return empty list on error
            assert result == []


# ============================================================================
# PARSING TESTS
# ============================================================================

class TestScoreboardParsing:
    """Test scoreboard data parsing"""

    def test_parse_scoreboard_data_success(self, api_client, sample_scoreboard_response):
        """Test parsing valid scoreboard data"""
        with patch.object(api_client, '_parse_game_event', return_value=Mock(spec=GameScore)):
            result = api_client._parse_scoreboard_data(sample_scoreboard_response)

            assert len(result) == 1
            api_client._parse_game_event.assert_called_once()

    def test_parse_scoreboard_data_empty_events(self, api_client):
        """Test parsing scoreboard with no events"""
        data = {'events': []}
        result = api_client._parse_scoreboard_data(data)

        assert result == []

    def test_parse_scoreboard_data_missing_events_key(self, api_client):
        """Test parsing scoreboard missing events key"""
        data = {}
        result = api_client._parse_scoreboard_data(data)

        assert result == []

    def test_parse_scoreboard_data_skips_invalid_events(self, api_client, sample_scoreboard_response):
        """Test parsing skips invalid event entries"""
        # Add invalid event (not a dict)
        sample_scoreboard_response['events'].append("invalid_event")
        sample_scoreboard_response['events'].append(None)

        with patch.object(api_client, '_parse_game_event', return_value=Mock(spec=GameScore)):
            result = api_client._parse_scoreboard_data(sample_scoreboard_response)

            # Should only parse the valid event
            assert api_client._parse_game_event.call_count == 1

    def test_parse_scoreboard_data_filters_by_completed(self, api_client, sample_scoreboard_response):
        """Test parsing filters by only_completed_games setting"""
        api_client.settings.only_completed_games = True

        mock_completed = Mock(spec=GameScore)
        mock_completed.is_completed = True

        mock_incomplete = Mock(spec=GameScore)
        mock_incomplete.is_completed = False

        with patch.object(api_client, '_parse_game_event', side_effect=[mock_completed, mock_incomplete]):
            # Add second event
            sample_scoreboard_response['events'].append(sample_scoreboard_response['events'][0])

            result = api_client._parse_scoreboard_data(sample_scoreboard_response)

            # Should only include completed game
            assert len(result) == 1
            assert result[0].is_completed == True


class TestGameEventParsing:
    """Test individual game event parsing"""

    def test_parse_game_event_success(self, api_client, sample_game_event):
        """Test parsing valid game event"""
        result = api_client._parse_game_event(sample_game_event)

        assert result is not None
        assert isinstance(result, GameScore)
        assert result.game_id == '401547416'
        assert result.week == 5
        assert result.season == 2025
        assert result.home_score == 24
        assert result.away_score == 17

    def test_parse_game_event_missing_id(self, api_client, sample_game_event):
        """Test parsing event missing game id"""
        del sample_game_event['id']

        result = api_client._parse_game_event(sample_game_event)

        assert result is None

    def test_parse_game_event_missing_date(self, api_client, sample_game_event):
        """Test parsing event missing date"""
        del sample_game_event['date']

        result = api_client._parse_game_event(sample_game_event)

        assert result is None

    def test_parse_game_event_no_competitions(self, api_client, sample_game_event):
        """Test parsing event with no competitions"""
        sample_game_event['competitions'] = []

        result = api_client._parse_game_event(sample_game_event)

        assert result is None

    def test_parse_game_event_wrong_competitor_count(self, api_client, sample_game_event):
        """Test parsing event with wrong number of competitors"""
        sample_game_event['competitions'][0]['competitors'] = [
            sample_game_event['competitions'][0]['competitors'][0]
        ]  # Only one team

        result = api_client._parse_game_event(sample_game_event)

        assert result is None

    def test_parse_game_event_missing_home_away_designation(self, api_client, sample_game_event):
        """Test parsing event without proper home/away designation"""
        # Both teams marked as away
        for competitor in sample_game_event['competitions'][0]['competitors']:
            competitor['homeAway'] = 'away'

        result = api_client._parse_game_event(sample_game_event)

        assert result is None

    def test_parse_game_event_extracts_venue_info(self, api_client, sample_game_event):
        """Test parsing extracts venue information"""
        result = api_client._parse_game_event(sample_game_event)

        assert result.venue_name == "AT&T Stadium"
        assert result.venue_city == "Arlington"
        assert result.venue_state == "TX"
        assert result.venue_capacity == 80000
        assert result.attendance == 75432

    def test_parse_game_event_extracts_weather(self, api_client, sample_game_event):
        """Test parsing extracts weather information"""
        result = api_client._parse_game_event(sample_game_event)

        assert result.temperature == 72
        assert result.weather_description == "Clear"

    def test_parse_game_event_extracts_statistics(self, api_client, sample_game_event):
        """Test parsing extracts team statistics"""
        result = api_client._parse_game_event(sample_game_event)

        assert result.home_total_yards == 385
        assert result.away_total_yards == 312
        assert result.home_turnovers == 1
        assert result.away_turnovers == 2

    def test_parse_game_event_extracts_quarter_scores(self, api_client, sample_game_event):
        """Test parsing extracts quarter-by-quarter scores"""
        result = api_client._parse_game_event(sample_game_event)

        assert result.home_score_q1 == 7
        assert result.home_score_q2 == 7
        assert result.home_score_q3 == 3
        assert result.home_score_q4 == 7

        assert result.away_score_q1 == 7
        assert result.away_score_q2 == 3
        assert result.away_score_q3 == 0
        assert result.away_score_q4 == 7

    def test_parse_game_event_handles_missing_optional_fields(self, api_client, sample_game_event):
        """Test parsing handles missing optional fields gracefully"""
        # Remove optional fields
        competition = sample_game_event['competitions'][0]
        del competition['venue']
        del competition['attendance']
        del competition['weather']
        del competition['broadcasts']

        result = api_client._parse_game_event(sample_game_event)

        assert result is not None
        assert result.venue_name is None
        assert result.attendance is None


class TestTeamParsing:
    """Test team data parsing"""

    def test_parse_team_data_success(self, api_client, sample_team_data):
        """Test parsing valid team data"""
        result = api_client._parse_team_data(sample_team_data)

        assert isinstance(result, Team)
        assert result.id == '1'
        assert result.name == 'Cowboys'
        assert result.display_name == 'Dallas Cowboys'
        assert result.abbreviation == 'DAL'
        assert result.location == 'Dallas'
        assert result.record == '8-2'

    def test_parse_team_data_missing_optional_fields(self, api_client):
        """Test parsing team with minimal data"""
        minimal_data = {
            'id': '1',
            'name': 'Cowboys',
            'displayName': 'Dallas Cowboys',
            'abbreviation': 'DAL',
            'location': 'Dallas'
        }

        result = api_client._parse_team_data(minimal_data)

        assert result.id == '1'
        assert result.color is None
        assert result.logo_url is None

    def test_parse_team_data_invalid_input(self, api_client):
        """Test parsing team with invalid input returns default team"""
        result = api_client._parse_team_data("not a dict")

        assert isinstance(result, Team)
        assert result.name == 'Unknown'


# ============================================================================
# UTILITY METHOD TESTS
# ============================================================================

class TestUtilityMethods:
    """Test utility parsing methods"""

    def test_extract_stat_found(self, api_client):
        """Test extracting existing statistic"""
        stats = [
            {'name': 'totalYards', 'displayValue': '385'},
            {'name': 'turnovers', 'displayValue': '2'}
        ]

        result = api_client._extract_stat(stats, 'totalYards')

        assert result == 385

    def test_extract_stat_not_found(self, api_client):
        """Test extracting non-existent statistic"""
        stats = [
            {'name': 'totalYards', 'displayValue': '385'}
        ]

        result = api_client._extract_stat(stats, 'penalties')

        assert result is None

    def test_extract_stat_invalid_value(self, api_client):
        """Test extracting statistic with invalid value"""
        stats = [
            {'name': 'totalYards', 'displayValue': 'N/A'}
        ]

        result = api_client._extract_stat(stats, 'totalYards')

        assert result is None

    def test_get_quarter_score_valid(self, api_client):
        """Test extracting valid quarter score"""
        line_scores = [
            {'value': 7},
            {'value': 10},
            {'value': 3},
            {'value': 7}
        ]

        result = api_client._get_quarter_score(line_scores, 1)

        assert result == 10

    def test_get_quarter_score_out_of_range(self, api_client):
        """Test extracting quarter score beyond available quarters"""
        line_scores = [
            {'value': 7},
            {'value': 10}
        ]

        result = api_client._get_quarter_score(line_scores, 3)

        assert result is None

    def test_get_quarter_score_invalid_value(self, api_client):
        """Test extracting quarter score with invalid value"""
        line_scores = [
            {'value': 'N/A'}
        ]

        result = api_client._get_quarter_score(line_scores, 0)

        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
