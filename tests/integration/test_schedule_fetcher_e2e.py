"""
Offline E2E integration test for the schedule fetcher pipeline (KAI-17 F3).

Invokes run_schedule_fetcher.py via subprocess with ESPN_FIXTURE_DIR set
to use fixture data, then asserts CSV output correctness.
"""
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

from schedule_data_fetcher.ScheduleFetcher import NFL_TEAMS as VALID_TEAMS

REPO_ROOT = Path(__file__).parent.parent.parent


@pytest.mark.offline
def test_schedule_fetcher_e2e(tmp_path: Path) -> None:
    """Run the schedule fetcher offline and assert CSV output correctness."""
    env = os.environ.copy()
    env["ESPN_FIXTURE_DIR"] = str(REPO_ROOT / "tests" / "fixtures")

    cmd = [
        sys.executable,
        str(REPO_ROOT / "run_schedule_fetcher.py"),
        "--season", "2025",
        "--output", str(tmp_path / "schedule.csv"),
    ]

    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)

    assert result.returncode == 0, result.stderr

    df = pd.read_csv(tmp_path / "schedule.csv", keep_default_na=False)

    assert list(df.columns) == ["week", "team", "opponent"]
    assert len(df) == 576
    assert set(df["team"].unique()) == VALID_TEAMS
    assert (df["opponent"] == "").any()


@pytest.mark.offline
def test_schedule_fetcher_skips_when_file_exists(tmp_path: Path) -> None:
    """Verify fetcher exits early without overwriting when output file already exists."""
    out = tmp_path / "schedule.csv"
    out.write_text("week,team,opponent\n1,KC,BAL\n")

    env = os.environ.copy()
    env["ESPN_FIXTURE_DIR"] = str(REPO_ROOT / "tests" / "fixtures")

    cmd = [
        sys.executable,
        str(REPO_ROOT / "run_schedule_fetcher.py"),
        "--season", "2025",
        "--output", str(out),
    ]

    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)

    assert result.returncode == 0
    assert "skipping fetch" in result.stderr or "skipping fetch" in result.stdout
    assert out.read_text() == "week,team,opponent\n1,KC,BAL\n"
