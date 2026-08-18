#!/usr/bin/env python3
"""
Player Data Fetcher Configuration

This file contains only non-CLI-configurable constants.
All CLI-configurable values (week, season, paths, flags, limits) are managed
via argparse defaults in run_player_fetcher.py.

Author: Kai Mizuno
"""

import os
from pathlib import Path


_DATA_ROOT = Path(__file__).parent.parent / 'data'


def data_root() -> Path:
    """The fetcher's data ROOT.

    This is the directory that CONTAINS player_data/, team_data/ and
    game_data.csv -- it is NOT the player_data/ subdirectory itself.

    Redirected by the PLAYER_DATA_DIR environment variable (the player-data
    parallel of LEAGUE_DATA_DIR, league_helper/LeagueHelperManager.py). When
    PLAYER_DATA_DIR is unset the repo-anchored default is returned, which is
    byte-identical to the historical value at every call site.

    Resolved on EVERY call, never at import/def time, so a caller that resolves
    its own defaults at construction time picks up a redirect set after import.
    """
    override = os.environ.get('PLAYER_DATA_DIR')
    return Path(override) if override else _DATA_ROOT


COORDINATES_JSON = Path(__file__).parent.parent / 'data' / 'coordinates.json'


LOG_NAME = "player_data_fetcher"
LOGGING_FORMAT = 'standard'

# The six position codes the package writes as data/player_data/{code}_data.json.
# Homed here rather than in player_data_fetcher_main so an offline consumer can
# reuse the single definition without importing the fetcher entrypoint's heavy
# runtime dependencies (pandas, ESPNClient). player_data_fetcher_main re-imports
# it, so player_data_fetcher_main.POSITION_CODES stays resolvable.
POSITION_CODES = ('qb', 'rb', 'wr', 'te', 'k', 'dst')

PROGRESS_ETA_WINDOW_SIZE = 50


ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


