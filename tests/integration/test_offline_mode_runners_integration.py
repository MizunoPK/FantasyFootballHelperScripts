#!/usr/bin/env python3
"""
Integration tests for offline_mode_runners feature (F2).

Tests ESPN_FIXTURE_DIR offline mode for ScheduleFetcher and BaseAPIClient.
All tests are fully offline — no live ESPN API calls made.
"""
import asyncio
import json
import types
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from tenacity import RetryError

project_root = Path(__file__).parent.parent.parent


class TestScheduleFetcherOfflineMode:

    @pytest.mark.asyncio
    async def test_returns_fixture_when_file_exists(self, monkeypatch, tmp_path):
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        fixture_data = {"events": [{"id": "401547353"}]}
        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()
        (espn_dir / "scoreboard_week_1_2025.json").write_text(json.dumps(fixture_data))

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        result = await fetcher._make_request(url, {"week": 1, "dates": 2025})

        assert result == fixture_data

    @pytest.mark.asyncio
    async def test_no_http_client_created_on_hit(self, monkeypatch, tmp_path):
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        fixture_data = {"events": []}
        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()
        (espn_dir / "scoreboard_week_3_2024.json").write_text(json.dumps(fixture_data))

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        await fetcher._make_request(url, {"week": 3, "dates": 2024})

        assert fetcher.client is None

    @pytest.mark.asyncio
    async def test_raises_file_not_found_on_miss(self, monkeypatch, tmp_path):
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        with pytest.raises(FileNotFoundError):
            await fetcher._make_request(url, {"week": 5, "dates": 2025})

    @pytest.mark.asyncio
    async def test_error_message_on_miss(self, monkeypatch, tmp_path):
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        with pytest.raises(FileNotFoundError) as exc_info:
            await fetcher._make_request(url, {"week": 5, "dates": 2025})

        assert "Fixture file not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_client_called_without_env_var(self, monkeypatch, tmp_path):
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)

        mock_response = MagicMock()
        mock_response.json.return_value = {"events": []}

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")

        async def fake_create_client():
            fetcher.client = mock_client

        monkeypatch.setattr(fetcher, "_create_client", fake_create_client)

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        await fetcher._make_request(url, {"week": 1, "dates": 2025})

        assert fetcher.client is mock_client


class TestBaseAPIClientOfflineMode:

    @pytest.mark.asyncio
    async def test_returns_fixture_when_file_exists(self, monkeypatch, tmp_path):
        from player_data_fetcher.espn_client import BaseAPIClient

        fixture_data = {"players": [{"id": "12345"}]}
        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()
        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        (espn_dir / "scoreboard_week_2_2025.json").write_text(json.dumps(fixture_data))

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)
        result = await client._make_request("GET", scoreboard_url, params={"week": 2, "dates": 2025})

        assert result == fixture_data

    @pytest.mark.asyncio
    async def test_no_asyncio_sleep_on_hit(self, monkeypatch, tmp_path):
        from player_data_fetcher.espn_client import BaseAPIClient

        fixture_data = {"players": []}
        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()
        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        (espn_dir / "scoreboard_week_4_2025.json").write_text(json.dumps(fixture_data))

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))
        mock_sleep = AsyncMock()
        monkeypatch.setattr(asyncio, "sleep", mock_sleep)

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)
        await client._make_request("GET", scoreboard_url, params={"week": 4, "dates": 2025})

        assert mock_sleep.call_count == 0

    @pytest.mark.asyncio
    async def test_raises_file_not_found_on_miss(self, monkeypatch, tmp_path):
        from player_data_fetcher.espn_client import BaseAPIClient

        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()
        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)
        with pytest.raises((FileNotFoundError, RetryError)):
            await client._make_request("GET", scoreboard_url, params={"week": 7, "dates": 2025})

    @pytest.mark.asyncio
    async def test_env_var_unset_calls_asyncio_sleep(self, monkeypatch, tmp_path):
        from player_data_fetcher.espn_client import BaseAPIClient

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        mock_sleep = AsyncMock()
        monkeypatch.setattr(asyncio, "sleep", mock_sleep)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"players": []}

        mock_http_client = AsyncMock()
        mock_http_client.request.return_value = mock_response

        settings = types.SimpleNamespace(rate_limit_delay=0.1, request_timeout=5.0)
        client = BaseAPIClient(settings)
        client._client = mock_http_client

        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        await client._make_request("GET", scoreboard_url, params={"week": 1, "dates": 2025})

        assert mock_sleep.call_count == 1


class TestGetFixtureFilename:

    def test_scoreboard_url(self):
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        params = {"week": 5, "dates": 2025}
        result = BaseAPIClient._get_fixture_filename(url, params)
        assert result == "scoreboard_week_5_2025.json"

    def test_teams_list_url(self):
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
        result = BaseAPIClient._get_fixture_filename(url, {})
        assert result == "teams_list.json"

    def test_team_stats_url(self):
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/22/statistics"
        result = BaseAPIClient._get_fixture_filename(url, {})
        assert result == "team_stats_22.json"

    def test_season_projections_url(self):
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/leaguedefaults/seasons/2025/segments/0/leaguetypes/0"
        result = BaseAPIClient._get_fixture_filename(url, {})
        assert result == "season_projections_2025.json"

    def test_unrecognized_url_raises_value_error(self):
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/unknown_endpoint"
        with pytest.raises(ValueError) as exc_info:
            BaseAPIClient._get_fixture_filename(url, {})
        assert "No fixture filename defined for URL" in str(exc_info.value)
