"""
Integration tests for offline_mode_runners feature (F2).

Tests ESPN_FIXTURE_DIR offline mode for ScheduleFetcher and BaseAPIClient.
All tests are fully offline — no live ESPN API calls made.
"""
import asyncio
import json
import types
from unittest.mock import AsyncMock, MagicMock
import pytest
from tenacity import RetryError


class TestScheduleFetcherOfflineMode:
    """Tests for ScheduleFetcher._make_request() offline mode via ESPN_FIXTURE_DIR."""

    @pytest.mark.asyncio
    async def test_returns_fixture_when_file_exists(self, monkeypatch, tmp_path):
        """Verify _make_request returns fixture JSON when ESPN_FIXTURE_DIR is set and file exists."""
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
        """Verify no HTTP client is created when fixture file is read (offline mode)."""
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
        """Verify FileNotFoundError is raised when fixture file is missing."""
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
        """Verify FileNotFoundError message includes 'Fixture file not found' context."""
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
        """Verify HTTP client is created (live path taken) when ESPN_FIXTURE_DIR is not set."""
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
    """Tests for BaseAPIClient._make_request() offline mode via ESPN_FIXTURE_DIR."""

    @pytest.mark.asyncio
    async def test_returns_fixture_when_file_exists(self, monkeypatch, tmp_path):
        """Verify _make_request returns fixture JSON when ESPN_FIXTURE_DIR is set and file exists."""
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
        """Verify asyncio.sleep is not called when fixture file is read (no rate limiting)."""
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
        """Verify FileNotFoundError is raised on the first attempt (non-retryable, not wrapped in RetryError) when the fixture is missing."""
        from player_data_fetcher.espn_client import BaseAPIClient

        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()
        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)
        with pytest.raises(FileNotFoundError):
            await client._make_request("GET", scoreboard_url, params={"week": 7, "dates": 2025})

    @pytest.mark.asyncio
    async def test_env_var_unset_calls_asyncio_sleep(self, monkeypatch, tmp_path):
        """Verify asyncio.sleep is called (live path taken) when ESPN_FIXTURE_DIR is not set."""
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

    @pytest.mark.asyncio
    async def test_offline_unmapped_url_value_error_fast_aborts(self, monkeypatch, tmp_path):
        """Offline: an unmapped-URL ValueError aborts on the first attempt (T53).

        The deterministic fixture-resolution ValueError must NOT be retried/backed-off in
        fixture mode: the raw ValueError propagates (a RetryError wrapper would not match
        pytest.raises(ValueError)) and no tenacity backoff sleep occurs.
        """
        from player_data_fetcher.espn_client import BaseAPIClient

        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()
        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))
        mock_sleep = AsyncMock()
        monkeypatch.setattr(asyncio, "sleep", mock_sleep)

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)
        unmapped_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/unknown_endpoint"

        with pytest.raises(ValueError) as exc_info:
            await client._make_request("GET", unmapped_url, params={})

        assert "No fixture filename defined for URL" in str(exc_info.value)
        assert mock_sleep.call_count == 0  # first-attempt abort, no retry/backoff loop

    @pytest.mark.asyncio
    async def test_offline_corrupt_fixture_json_error_fast_aborts(self, monkeypatch, tmp_path):
        """Offline: a corrupt-fixture json.JSONDecodeError aborts on the first attempt (T53).

        json.JSONDecodeError subclasses ValueError; in fixture mode it must fast-abort with
        no retry/backoff. A RetryError wrapper would not match pytest.raises(json.JSONDecodeError).
        """
        from player_data_fetcher.espn_client import BaseAPIClient

        espn_dir = tmp_path / "espn_api"
        espn_dir.mkdir()
        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        (espn_dir / "scoreboard_week_6_2025.json").write_text("{ this is not valid json")

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))
        mock_sleep = AsyncMock()
        monkeypatch.setattr(asyncio, "sleep", mock_sleep)

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)

        with pytest.raises(json.JSONDecodeError):
            await client._make_request("GET", scoreboard_url, params={"week": 6, "dates": 2025})

        assert mock_sleep.call_count == 0  # first-attempt abort, no retry/backoff loop

    @pytest.mark.asyncio
    async def test_live_transient_error_still_retried(self, monkeypatch, tmp_path):
        """Live path (ESPN_FIXTURE_DIR unset): a transient ESPNServerError is STILL retried 3x.

        Positive control proving the offline ValueError exclusion did not leak into the live
        path (offline-confinement — D2/D4). asyncio.sleep is mocked so the retry loop is instant.
        """
        from player_data_fetcher.espn_client import BaseAPIClient, ESPNServerError

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        mock_sleep = AsyncMock()
        monkeypatch.setattr(asyncio, "sleep", mock_sleep)

        mock_response = MagicMock()
        mock_response.status_code = 500

        mock_http_client = AsyncMock()
        mock_http_client.request.return_value = mock_response

        settings = types.SimpleNamespace(rate_limit_delay=0.1, request_timeout=5.0)
        client = BaseAPIClient(settings)
        client._client = mock_http_client

        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        with pytest.raises(RetryError):
            await client._make_request("GET", scoreboard_url, params={"week": 1, "dates": 2025})

        assert mock_http_client.request.call_count == 3  # transient set still retried 3x

    @pytest.mark.asyncio
    async def test_live_response_json_decode_error_still_retried(self, monkeypatch, tmp_path):
        """Live path (ESPN_FIXTURE_DIR unset): a response.json() JSONDecodeError is STILL retried.

        The decisive D2 positive control: the live malformed-body JSONDecodeError (a ValueError
        subclass) must keep retrying — the env gate confines the offline ValueError exclusion so
        it never fires here. An unconditional ValueError exclusion (Option A) would fail this.
        """
        from player_data_fetcher.espn_client import BaseAPIClient

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        mock_sleep = AsyncMock()
        monkeypatch.setattr(asyncio, "sleep", mock_sleep)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)

        mock_http_client = AsyncMock()
        mock_http_client.request.return_value = mock_response

        settings = types.SimpleNamespace(rate_limit_delay=0.1, request_timeout=5.0)
        client = BaseAPIClient(settings)
        client._client = mock_http_client

        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        with pytest.raises(RetryError):
            await client._make_request("GET", scoreboard_url, params={"week": 1, "dates": 2025})

        assert mock_http_client.request.call_count == 3  # live JSONDecodeError still retried (D2)


class TestGetFixtureFilename:
    """Tests for BaseAPIClient._get_fixture_filename() URL-to-fixture-filename mapping."""

    def test_scoreboard_url(self):
        """Verify scoreboard URL maps to scoreboard_week_{N}_{YYYY}.json."""
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        params = {"week": 5, "dates": 2025}
        result = BaseAPIClient._get_fixture_filename(url, params)
        assert result == "scoreboard_week_5_2025.json"

    def test_teams_list_url(self):
        """Verify teams list URL maps to teams_list.json."""
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
        result = BaseAPIClient._get_fixture_filename(url, {})
        assert result == "teams_list.json"

    def test_team_stats_url(self):
        """Verify team stats URL maps to team_stats_{id}.json with extracted team ID."""
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/22/statistics"
        result = BaseAPIClient._get_fixture_filename(url, {})
        assert result == "team_stats_22.json"

    def test_season_projections_url(self):
        """Verify leaguedefaults URL maps to season_projections_{season}.json with extracted year."""
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/leaguedefaults/seasons/2025/segments/0/leaguetypes/0"
        result = BaseAPIClient._get_fixture_filename(url, {})
        assert result == "season_projections_2025.json"

    def test_unrecognized_url_raises_value_error(self):
        """Verify unrecognized URL raises ValueError with descriptive message."""
        from player_data_fetcher.espn_client import BaseAPIClient

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/unknown_endpoint"
        with pytest.raises(ValueError) as exc_info:
            BaseAPIClient._get_fixture_filename(url, {})
        assert "No fixture filename defined for URL" in str(exc_info.value)


