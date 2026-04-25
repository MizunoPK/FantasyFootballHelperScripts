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

REPO_ROOT = Path(__file__).parent.parent.parent

VALID_TEAMS = frozenset({
    'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
    'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
    'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
    'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH',
})


@pytest.mark.offline
def test_schedule_fetcher_e2e(tmp_path):
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
    assert set(df["team"].unique()).issubset(VALID_TEAMS)
    assert (df["opponent"].isna() | (df["opponent"] == "")).any()
