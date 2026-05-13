"""
E2E integration test for compile_historical_data.py (FF-1 F06).

Invokes compile_historical_data.py --year 2025 via subprocess with ESPN_FIXTURE_DIR
set to use fixture data, then asserts output directory structure and file contents.
Also verifies that BaseHTTPClient.get() raises FileNotFoundError when ESPN_FIXTURE_DIR
is set but the requested fixture file is missing.
"""
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from historical_data_compiler.constants import VALIDATION_WEEKS
from historical_data_compiler.http_client import BaseHTTPClient

REPO_ROOT = Path(__file__).parent.parent.parent


@pytest.mark.offline
def test_compile_historical_data_e2e(tmp_path: Path) -> None:
    """Run compile_historical_data.py offline and assert output structure correctness."""
    output_dir = tmp_path / "sim_data" / "2025"
    env = os.environ.copy()
    env["ESPN_FIXTURE_DIR"] = str(REPO_ROOT / "tests" / "fixtures")

    cmd = [
        sys.executable,
        str(REPO_ROOT / "compile_historical_data.py"),
        "--year", "2025",
        "--output-dir", str(output_dir),
    ]
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=120)

    assert result.returncode == 0, result.stderr
    assert (output_dir / "season_schedule.csv").exists()
    assert (output_dir / "game_data.csv").exists()

    weeks_dir = output_dir / "weeks"
    for week in range(1, VALIDATION_WEEKS + 1):
        week_dir = weeks_dir / f"week_{week:02d}"
        assert week_dir.exists()
        for pos in ["qb", "rb", "wr", "te", "k", "dst"]:
            json_path = week_dir / f"{pos}_data.json"
            assert json_path.exists()
            data = json.loads(json_path.read_text())
            assert f"{pos}_data" in data
            assert len(data[f"{pos}_data"]) >= 1


@pytest.mark.offline
def test_missing_fixture_raises_file_not_found(tmp_path: Path) -> None:
    """Verify FileNotFoundError when ESPN_FIXTURE_DIR is set but fixture file is missing."""
    with patch.dict(os.environ, {"ESPN_FIXTURE_DIR": str(tmp_path)}):
        client = BaseHTTPClient()
        with pytest.raises(FileNotFoundError, match="Fixture file not found"):
            asyncio.run(client.get(
                "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
                params={"week": 1, "dates": 2025},
            ))


@pytest.mark.offline
def test_missing_fixture_raises_file_not_found_fantasy(tmp_path: Path) -> None:
    """Verify FileNotFoundError when ESPN_FIXTURE_DIR is set but fantasy fixture is missing."""
    with patch.dict(os.environ, {"ESPN_FIXTURE_DIR": str(tmp_path)}):
        client = BaseHTTPClient()
        with pytest.raises(FileNotFoundError, match="Fixture file not found"):
            asyncio.run(client.get(
                "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3",
            ))
