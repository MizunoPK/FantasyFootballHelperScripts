"""
Shared ConfigManager Test-Config Fixtures

Test-support definitions shared by the ConfigManager legacy-config test modules.
`league_params` and `_write_legacy_config` were byte-identical duplicates in
test_ConfigManager_tier_reachability.py (D5.1) and test_ConfigManager_linear_scaling.py
(D10.1); LEAGUE_FIXTURE travels with them because league_params' body reads it.

Not a test module -- the basename matches no `test_*.py` pattern, so pytest collects
nothing here. Consumers import these symbols explicitly at module level, which places
`league_params` in the importing module's own namespace where pytest collects it as a
fixture, and leaves `_write_legacy_config` callable unqualified exactly as before.

Author: Claude Code
Date: 2026-08-17
"""

import json
from pathlib import Path

import pytest


LEAGUE_FIXTURE = Path("tests/fixtures/league/league_config.json")


@pytest.fixture
def league_params():
    """A complete, guard-clean legacy config, re-read so a test may mutate it freely."""
    return json.loads(LEAGUE_FIXTURE.read_text())


def _write_legacy_config(tmp_path, data):
    """Write `data` as a legacy single-file config; return the data folder."""
    (tmp_path / "league_config.json").write_text(json.dumps(data))
    return tmp_path
