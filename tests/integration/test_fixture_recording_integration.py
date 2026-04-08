"""
Integration tests for fixture_recording feature (F3).

Tests ESPN_RECORD_FIXTURES_DIR recording mechanism for ScheduleFetcher and BaseAPIClient.
All tests are fully offline — no live ESPN API calls made.
"""
import json
import types
from unittest.mock import AsyncMock, MagicMock
import pytest


class TestScheduleFetcherRecording:
    """Tests for ScheduleFetcher._make_request() recording via ESPN_RECORD_FIXTURES_DIR."""

    @pytest.mark.asyncio
    async def test_recording_writes_file_when_env_var_set(self, monkeypatch, tmp_path):
        """Verify fixture file written with correct content when ESPN_RECORD_FIXTURES_DIR is set."""
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        fixture_data = {"events": [{"id": "401547353"}]}
        record_dir = tmp_path / "records"
        record_dir.mkdir()

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.setenv("ESPN_RECORD_FIXTURES_DIR", str(record_dir))

        mock_response = MagicMock()
        mock_response.json.return_value = fixture_data
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")

        async def fake_create_client():
            fetcher.client = mock_client

        monkeypatch.setattr(fetcher, "_create_client", fake_create_client)

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        result = await fetcher._make_request(url, {"week": 1, "dates": 2025})

        expected_path = record_dir / "espn_api" / "scoreboard_week_1_2025.json"
        assert expected_path.exists()
        assert json.loads(expected_path.read_text()) == fixture_data
        assert result == fixture_data

    @pytest.mark.asyncio
    async def test_recording_creates_directory_if_missing(self, monkeypatch, tmp_path):
        """Verify espn_api/ subdir is auto-created when target directory doesn't exist."""
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        fixture_data = {"events": []}
        record_dir = tmp_path / "new_records"

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.setenv("ESPN_RECORD_FIXTURES_DIR", str(record_dir))

        mock_response = MagicMock()
        mock_response.json.return_value = fixture_data
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")

        async def fake_create_client():
            fetcher.client = mock_client

        monkeypatch.setattr(fetcher, "_create_client", fake_create_client)

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        await fetcher._make_request(url, {"week": 2, "dates": 2025})

        espn_dir = record_dir / "espn_api"
        assert espn_dir.exists()
        assert (espn_dir / "scoreboard_week_2_2025.json").exists()

    @pytest.mark.asyncio
    async def test_no_recording_when_env_var_not_set(self, monkeypatch, tmp_path):
        """Verify no files are written when ESPN_RECORD_FIXTURES_DIR is not set."""
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        fixture_data = {"events": []}

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.delenv("ESPN_RECORD_FIXTURES_DIR", raising=False)

        mock_response = MagicMock()
        mock_response.json.return_value = fixture_data
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")

        async def fake_create_client():
            fetcher.client = mock_client

        monkeypatch.setattr(fetcher, "_create_client", fake_create_client)

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        result = await fetcher._make_request(url, {"week": 3, "dates": 2025})

        assert result == fixture_data
        assert not list(tmp_path.rglob("*.json"))

    @pytest.mark.asyncio
    async def test_recording_overwrites_existing_file(self, monkeypatch, tmp_path):
        """Verify recording overwrites existing fixture file rather than appending."""
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        old_data = {"events": [{"id": "OLD"}]}
        new_data = {"events": [{"id": "NEW"}]}
        record_dir = tmp_path / "records"
        espn_dir = record_dir / "espn_api"
        espn_dir.mkdir(parents=True)
        (espn_dir / "scoreboard_week_1_2025.json").write_text(json.dumps(old_data))

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.setenv("ESPN_RECORD_FIXTURES_DIR", str(record_dir))

        mock_response = MagicMock()
        mock_response.json.return_value = new_data
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")

        async def fake_create_client():
            fetcher.client = mock_client

        monkeypatch.setattr(fetcher, "_create_client", fake_create_client)

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        await fetcher._make_request(url, {"week": 1, "dates": 2025})

        written = json.loads((espn_dir / "scoreboard_week_1_2025.json").read_text())
        assert written == new_data
        assert written != old_data

    @pytest.mark.asyncio
    async def test_no_recording_when_offline_mode_active(self, monkeypatch, tmp_path):
        """Verify no recording happens when ESPN_FIXTURE_DIR is set (F2 offline returns early)."""
        from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher

        fixture_data = {"events": [{"id": "OFFLINE"}]}
        fixture_dir = tmp_path / "fixtures"
        espn_fixture_dir = fixture_dir / "espn_api"
        espn_fixture_dir.mkdir(parents=True)
        (espn_fixture_dir / "scoreboard_week_1_2025.json").write_text(json.dumps(fixture_data))

        record_dir = tmp_path / "records"
        record_dir.mkdir()

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(fixture_dir))
        monkeypatch.setenv("ESPN_RECORD_FIXTURES_DIR", str(record_dir))

        fetcher = ScheduleFetcher(output_path=tmp_path / "schedule.csv")
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        await fetcher._make_request(url, {"week": 1, "dates": 2025})

        assert not list(record_dir.rglob("*.json"))


class TestBaseAPIClientRecording:
    """Tests for BaseAPIClient._make_request() recording via ESPN_RECORD_FIXTURES_DIR."""

    @pytest.mark.asyncio
    async def test_recording_writes_file_when_env_var_set(self, monkeypatch, tmp_path):
        """Verify fixture file written with correct content when ESPN_RECORD_FIXTURES_DIR is set."""
        from player_data_fetcher.espn_client import BaseAPIClient

        fixture_data = {"players": [{"id": "12345"}]}
        record_dir = tmp_path / "records"
        record_dir.mkdir()

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.setenv("ESPN_RECORD_FIXTURES_DIR", str(record_dir))

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fixture_data
        mock_http_client = AsyncMock()
        mock_http_client.request.return_value = mock_response

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)
        client._client = mock_http_client

        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        result = await client._make_request("GET", scoreboard_url, params={"week": 1, "dates": 2025})

        expected_path = record_dir / "espn_api" / "scoreboard_week_1_2025.json"
        assert expected_path.exists()
        assert json.loads(expected_path.read_text()) == fixture_data
        assert result == fixture_data

    @pytest.mark.asyncio
    async def test_recording_creates_directory_if_missing(self, monkeypatch, tmp_path):
        """Verify espn_api/ subdir is auto-created when target directory doesn't exist."""
        from player_data_fetcher.espn_client import BaseAPIClient

        fixture_data = {"players": []}
        record_dir = tmp_path / "new_records"

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.setenv("ESPN_RECORD_FIXTURES_DIR", str(record_dir))

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fixture_data
        mock_http_client = AsyncMock()
        mock_http_client.request.return_value = mock_response

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)
        client._client = mock_http_client

        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        await client._make_request("GET", scoreboard_url, params={"week": 2, "dates": 2025})

        espn_dir = record_dir / "espn_api"
        assert espn_dir.exists()
        assert (espn_dir / "scoreboard_week_2_2025.json").exists()

    @pytest.mark.asyncio
    async def test_no_recording_when_env_var_not_set(self, monkeypatch, tmp_path):
        """Verify no files are written when ESPN_RECORD_FIXTURES_DIR is not set."""
        from player_data_fetcher.espn_client import BaseAPIClient

        fixture_data = {"players": []}

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.delenv("ESPN_RECORD_FIXTURES_DIR", raising=False)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fixture_data
        mock_http_client = AsyncMock()
        mock_http_client.request.return_value = mock_response

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)
        client._client = mock_http_client

        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        result = await client._make_request("GET", scoreboard_url, params={"week": 3, "dates": 2025})

        assert result == fixture_data
        assert not list(tmp_path.rglob("*.json"))

    @pytest.mark.asyncio
    async def test_recording_overwrites_existing_file(self, monkeypatch, tmp_path):
        """Verify recording overwrites existing fixture file rather than appending."""
        from player_data_fetcher.espn_client import BaseAPIClient

        old_data = {"players": [{"id": "OLD"}]}
        new_data = {"players": [{"id": "NEW"}]}
        record_dir = tmp_path / "records"
        espn_dir = record_dir / "espn_api"
        espn_dir.mkdir(parents=True)
        (espn_dir / "scoreboard_week_1_2025.json").write_text(json.dumps(old_data))

        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.setenv("ESPN_RECORD_FIXTURES_DIR", str(record_dir))

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = new_data
        mock_http_client = AsyncMock()
        mock_http_client.request.return_value = mock_response

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)
        client._client = mock_http_client

        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        await client._make_request("GET", scoreboard_url, params={"week": 1, "dates": 2025})

        written = json.loads((espn_dir / "scoreboard_week_1_2025.json").read_text())
        assert written == new_data
        assert written != old_data

    @pytest.mark.asyncio
    async def test_no_recording_when_offline_mode_active(self, monkeypatch, tmp_path):
        """Verify no recording happens when ESPN_FIXTURE_DIR is set (F2 offline returns early)."""
        from player_data_fetcher.espn_client import BaseAPIClient

        fixture_data = {"players": [{"id": "OFFLINE"}]}
        fixture_dir = tmp_path / "fixtures"
        espn_fixture_dir = fixture_dir / "espn_api"
        espn_fixture_dir.mkdir(parents=True)
        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        (espn_fixture_dir / "scoreboard_week_1_2025.json").write_text(json.dumps(fixture_data))

        record_dir = tmp_path / "records"
        record_dir.mkdir()

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(fixture_dir))
        monkeypatch.setenv("ESPN_RECORD_FIXTURES_DIR", str(record_dir))

        settings = types.SimpleNamespace(rate_limit_delay=0.0, request_timeout=5.0)
        client = BaseAPIClient(settings)

        await client._make_request("GET", scoreboard_url, params={"week": 1, "dates": 2025})

        assert not list(record_dir.rglob("*.json"))


