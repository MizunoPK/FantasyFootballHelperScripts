"""
E2E integration test for the league helper application.

Invokes run_league_helper.py via subprocess with scripted stdin and a temp
fixture data directory assembled at runtime. Asserts exit code 0, no Python
traceback in stderr, startup banner in stdout, and evidence of add-to-roster
mode navigation.
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


def _assemble_data_dir(tmp_path: Path) -> dict:
    """
    Assemble a temp LEAGUE_DATA_DIR from the committed offline fixtures.

    Args:
        tmp_path (Path): Pytest-provided temporary directory, cleaned up after test.

    Returns:
        dict: A copy of os.environ with LEAGUE_DATA_DIR pointed at the temp tree, so
            every write the app performs lands there and the tracked data/ is untouched.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    shutil.copy(FIXTURE_LEAGUE_CONFIG, data_dir / "league_config.json")
    shutil.copytree(FIXTURE_PLAYER_DATA, data_dir / "player_data")

    env = os.environ.copy()
    env["LEAGUE_DATA_DIR"] = str(data_dir)
    return env


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
        env = _assemble_data_dir(tmp_path)

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

    def test_eof_at_main_menu_exits_cleanly_without_a_traceback(self, tmp_path: Path) -> None:
        """
        Verify a closed stdin ends the session with one notice line and no traceback (T83 R1).

        This is the T83 reproduction made permanent: stdin is closed immediately, so
        EOF lands at the MAIN MENU prompt.

        NOTE ON WHAT DISCRIMINATES: an unfixed build ALSO exits 1 here (by unhandled
        EOFError), so the exit code cannot tell a fixed build from a broken one. The
        discriminating assertions are the notice PRESENCE and the traceback ABSENCE.
        The returncode assertion guards against the wrong status instead (e.g. a fix
        that treated EOF as Quit and exited 0).

        Args:
            tmp_path (Path): Pytest-provided temporary directory, cleaned up after test.
        """
        env = _assemble_data_dir(tmp_path)

        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "run_league_helper.py")],
            input=b"",
            capture_output=True,
            timeout=60,
            env=env,
        )

        stdout = result.stdout.decode()
        stderr = result.stderr.decode()

        assert result.returncode == 1, f"Expected exit code 1, got {result.returncode}. stderr: {stderr}"
        # LoggingManager prefixes the line and writes it to stdout -- substring match only.
        assert "No input available on stdin — exiting." in stdout, f"Notice missing. stdout: {stdout[-2000:]}"
        assert "Traceback (most recent call last):" not in stderr, f"Python traceback found in stderr: {stderr}"

    def test_eof_in_modify_player_data_does_not_claim_a_return_to_the_menu(self, tmp_path: Path) -> None:
        """
        Verify EOF inside Modify Player Data ends the session instead of announcing a return (T83 R2a).

        Driving `4` enters Modify Player Data, whose submenu prompt then meets the
        exhausted pipe. Before T83 this printed "Input stream closed. Returning to
        Main Menu..." and went back to the Main Menu, which immediately re-prompted
        the same dead stream and died there with a traceback. The stale line is now
        gone and the session ends at the single notice.

        Args:
            tmp_path (Path): Pytest-provided temporary directory, cleaned up after test.
        """
        env = _assemble_data_dir(tmp_path)

        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "run_league_helper.py")],
            input=b"4\n",
            capture_output=True,
            timeout=60,
            env=env,
        )

        stdout = result.stdout.decode()
        stderr = result.stderr.decode()

        assert result.returncode == 1, f"Expected exit code 1, got {result.returncode}. stderr: {stderr}"
        assert "MODIFY PLAYER DATA" in stdout.upper(), f"Never reached Modify Player Data. stdout: {stdout[-2000:]}"
        assert "Input stream closed. Returning to Main Menu" not in stdout, \
            f"Stale return-to-menu line survived. stdout: {stdout[-2000:]}"
        assert "No input available on stdin — exiting." in stdout, f"Notice missing. stdout: {stdout[-2000:]}"
        assert "Traceback (most recent call last):" not in stderr, f"Python traceback found in stderr: {stderr}"

    def test_eof_at_a_bare_input_outside_the_menu_helper_also_exits_cleanly(self, tmp_path: Path) -> None:
        """
        Verify the fix is not show_list_selection-scoped (T83 R1, propagation-only site).

        Driving `2` enters Starter Helper, which renders its recommendation list and stops
        at the bare `input()` behind `Press Enter to Continue...`
        (StarterHelperModeManager.py:311) -- a prompt OUTSIDE the shared menu helper and
        outside every try. This is the automated guard for the six propagation-only prompt
        sites (that one plus TradeSimulatorModeManager.py:132,528,580,604,631), which are
        otherwise covered only by the Phase-6 user test plan and not by
        `python tests/run_all_tests.py`.

        Args:
            tmp_path (Path): Pytest-provided temporary directory, cleaned up after test.
        """
        env = _assemble_data_dir(tmp_path)

        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "run_league_helper.py")],
            input=b"2\n",
            capture_output=True,
            timeout=60,
            env=env,
        )

        stdout = result.stdout.decode()
        stderr = result.stderr.decode()

        assert result.returncode == 1, f"Expected exit code 1, got {result.returncode}. stderr: {stderr}"
        assert "STARTER HELPER" in stdout.upper(), f"Never reached Starter Helper. stdout: {stdout[-2000:]}"
        assert "No input available on stdin — exiting." in stdout, f"Notice missing. stdout: {stdout[-2000:]}"
        assert "Traceback (most recent call last):" not in stderr, f"Python traceback found in stderr: {stderr}"
