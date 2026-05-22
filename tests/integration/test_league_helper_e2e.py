"""
E2E integration test for the league helper application (FF-4 F07).

Invokes run_league_helper.py via subprocess with scripted stdin and a temp
fixture data directory assembled at runtime. Asserts exit code 0, no Python
traceback in stderr, startup banner in stdout, and evidence of add-to-roster
mode navigation.

Test Category: R1-R9 — E2E subprocess invocation (1 test)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent.parent
FIXTURE_PLAYER_DATA = REPO_ROOT / "tests" / "fixtures" / "player_data"
FIXTURE_LEAGUE_CONFIG = REPO_ROOT / "tests" / "fixtures" / "league" / "league_config.json"


@pytest.mark.offline
class TestLeagueHelperE2E:
    """
    End-to-end tests for the league helper application via subprocess invocation.

    Assembles a temp fixture data directory at test runtime from pre-built fixture
    files, then invokes run_league_helper.py with scripted stdin to drive a
    non-trivial mode path (add-to-roster → back to menu → quit).
    """

    def test_league_helper_runs_e2e(self, tmp_path: Path) -> None:
        """
        Verify the league helper starts, navigates add-to-roster mode, and exits cleanly.

        Args:
            tmp_path (Path): Pytest-provided temporary directory, cleaned up after test.
        """
        data_dir = tmp_path / "data"
        data_dir.mkdir()

        shutil.copy(FIXTURE_LEAGUE_CONFIG, data_dir / "league_config.json")
        shutil.copytree(FIXTURE_PLAYER_DATA, data_dir / "player_data")

        env = os.environ.copy()
        env["LEAGUE_DATA_DIR"] = str(data_dir)

        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "run_league_helper.py")],
            input=b"1\n6\n6\n",
            capture_output=True,
            timeout=60,
            env=env,
        )

        stdout = result.stdout.decode()
        stderr = result.stderr.decode()

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}. stderr: {stderr}"
        assert "Traceback (most recent call last):" not in stderr, f"Python traceback found in stderr: {stderr}"
        assert "Config:" in stdout, f"Expected startup banner 'Config:' in stdout. stdout: {stdout}"
        assert "ADD TO ROSTER" in stdout, f"Expected 'ADD TO ROSTER' mode header in stdout. stdout: {stdout}"
