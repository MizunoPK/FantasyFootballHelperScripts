"""
Repository-hygiene tests for the .env credential store (D17.1, TD4)

Asserts .env.example's exact committed shape and that .env itself stays
ignored, unindexed, and absent from history -- the executable regression
guard for TD4's "credential-only .env, non-secret identity elsewhere" split.

Author: Kai Mizuno
"""

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _run_git(*args):
    return subprocess.run(
        ['git', *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class TestEnvExampleShape:
    """.env.example carries exactly espn_s2= and SWID=, no values."""

    def test_env_example_exists(self):
        assert (REPO_ROOT / '.env.example').is_file()

    def test_env_example_exact_content(self):
        content = (REPO_ROOT / '.env.example').read_text()
        assert content == 'espn_s2=\nSWID=\n'

    def test_env_example_carries_no_values(self):
        content = (REPO_ROOT / '.env.example').read_text()
        for line in content.splitlines():
            key, _, value = line.partition('=')
            assert value == '', f"{key} carries a non-empty value in .env.example"


class TestEnvIgnoredUnindexedHistoryless:
    """.env stays gitignored, unindexed, and absent from history."""

    def test_env_is_gitignored(self):
        result = _run_git('check-ignore', '-v', '.env')
        assert result.returncode == 0, (
            f".env is not covered by an ignore rule (git check-ignore exit "
            f"{result.returncode}): {result.stdout}{result.stderr}"
        )
        assert result.stdout.startswith('.gitignore:'), (
            f"expected the match to come from .gitignore, got: {result.stdout!r}"
        )
        assert result.stdout.strip().endswith('\t.env'), (
            f"expected the matched pathspec to be exactly '.env' (not e.g. "
            f".env.example or a substring hit), got: {result.stdout!r}"
        )

    def test_env_is_not_tracked(self):
        result = _run_git('ls-files', '.env')
        assert result.stdout.strip() == '', (
            f".env is tracked by git: {result.stdout}"
        )

    def test_env_untracked_state_is_actually_the_protected_ignored_state(self):
        """Being untracked must coincide with being LIVE-matched by an ignore
        rule right now, not merely absent from the index for some unrelated
        reason (e.g. a manual `git rm --cached .env` run after the ignore
        rule itself was since weakened or removed -- that leaves `git
        ls-files .env` empty exactly like the healthy case, so that check
        alone cannot tell the two apart). `git status --porcelain
        --ignored=matching -- .env` reports a currently-untracked,
        currently-ignore-matched path as the single line `!! .env`; anything
        else (blank, or a bare `?? .env`) means untracked-but-unprotected."""
        if not (REPO_ROOT / '.env').is_file():
            pytest.skip(".env absent on this checkout (expected on a fresh clone); "
                        "the ignore-match assertion below needs a present path to be non-vacuous")
        result = _run_git('status', '--porcelain', '--ignored=matching', '--', '.env')
        assert result.stdout.strip() == '!! .env', (
            f"expected .env to report as currently ignored+untracked "
            f"('!! .env'), got: {result.stdout!r}"
        )

    def test_env_has_no_history(self):
        result = _run_git('log', '--all', '--', '.env')
        assert result.stdout.strip() == '', (
            f".env has commit history: {result.stdout}"
        )
