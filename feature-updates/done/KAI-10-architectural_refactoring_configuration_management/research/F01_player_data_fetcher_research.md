## Research Notes: Feature 01 — refactor_player_data_fetcher

**Created:** 2026-02-18 (S2.P1.I1)
**Feature:** feature_01_refactor_player_data_fetcher

---

## Files Researched

### 1. `run_player_fetcher.py` (Runner Script)

**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/run_player_fetcher.py`

**Current architecture:**
- Uses `subprocess.run()` + `os.chdir(fetcher_dir)` to invoke `player_data_fetcher_main.py` as a subprocess
- Has `argparse` with `parse_known_args()` — only `--enable-log-file` currently
- Forwards ALL `sys.argv[1:]` to the subprocess
- This means player_data_fetcher_main.py ALSO has its own argparse

**Key insight:** The subprocess approach creates TWO argparse instances. The notes "After" pattern shows direct `asyncio.run(main(settings_dict))` — this implies replacing subprocess with direct import.

### 2. `player-data-fetcher/player_data_fetcher_main.py` (Main Module)

**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/player-data-fetcher/player_data_fetcher_main.py`

**Current architecture:**
- Has its own `argparse` in `main()` with `--enable-log-file` only
- Has `Settings(BaseSettings)` class using pydantic_settings (env_prefix='NFL_PROJ_')
  - Fields: `season=NFL_SEASON`, `current_nfl_week=CURRENT_NFL_WEEK`, `request_timeout=REQUEST_TIMEOUT`, `rate_limit_delay=RATE_LIMIT_DELAY`
  - Missing many CLI-configurable fields (player_limit, paths, feature flags)
- `NFLProjectionsCollector.__init__(settings: Settings)` — ALREADY has constructor pattern ✅
- BUT `save_to_historical_data()` uses bare `ENABLE_HISTORICAL_DATA_SAVE`, `CURRENT_NFL_WEEK`, `NFL_SEASON` from config (not self.settings) ⚠️
- `fetch_game_data()` checks `ENABLE_GAME_DATA_FETCH` from config (not self.settings) ⚠️
- Config imports at module level: `NFL_SEASON, CURRENT_NFL_WEEK, REQUEST_TIMEOUT, RATE_LIMIT_DELAY, LOGGING_LEVEL, LOG_NAME, LOGGING_FORMAT, ENABLE_HISTORICAL_DATA_SAVE, ENABLE_GAME_DATA_FETCH`

**Methods needing fix:**
- `save_to_historical_data()`: Uses `ENABLE_HISTORICAL_DATA_SAVE`, `CURRENT_NFL_WEEK`, `NFL_SEASON` — must use `self.settings.*`
- `fetch_game_data()`: Uses `ENABLE_GAME_DATA_FETCH` — must use `self.settings.enable_game_data`
- `main()`: Must accept `settings_dict: dict | None = None` parameter

### 3. `player-data-fetcher/espn_client.py` (ESPN API Client)

**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/player-data-fetcher/espn_client.py`

**Config imports:**
- Top-level (line 27): `from config import (ESPN_USER_AGENT, ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK)`
- SCATTERED INLINE in methods (lines 617, 651, 914, 981, 1068, 1469, 1878):
  - `from config import CURRENT_NFL_WEEK, NFL_SEASON`
  - `from config import NFL_SEASON`
  - `from config import CURRENT_NFL_WEEK`
  - `from config import (PROGRESS_UPDATE_FREQUENCY, PROGRESS_ETA_WINDOW_SIZE, CURRENT_NFL_WEEK)`

**Usage of constants:**
- `ESPN_USER_AGENT` (non-CLI, stays in config): Used in request headers (lines 586, 600)
- `ESPN_PLAYER_LIMIT` (CLI arg → `--espn-player-limit`): Used in X-Fantasy-Filter header (line 587)
- `CURRENT_NFL_WEEK` (CLI arg → `--week`): Used extensively throughout (lines 320, 332, 368, 616, 621-642, 914, 922, 965, 1469-1502, 1878)
- `NFL_SEASON` (CLI arg → `--season`): Used in multiple methods

**Refactoring challenge:** High complexity. 10+ scattered inline imports need to be replaced with `self.settings.*` attributes. ESPNClient already receives settings via constructor.

**BaseAPIClient.__init__:** Takes `settings` and accesses `settings.request_timeout` and `settings.rate_limit_delay` (lines 60-70).

### 4. `player-data-fetcher/player_data_exporter.py` (Data Exporter)

**Location:** `/home/kai/code/FantasyFootballHelperScriptsRefactored/player-data-fetcher/player_data_exporter.py`

**Config imports (line 27):** `from config import POSITION_JSON_OUTPUT, CURRENT_NFL_WEEK, TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME`

**Usage:**
- `__init__`: Uses `DRAFTED_DATA`, `MY_TEAM_NAME` in DraftedRosterManager constructor (line 53); `LOAD_DRAFTED_DATA_FROM_FILE` to decide whether to load (line 54)
- `export_position_json_files()`: Uses `POSITION_JSON_OUTPUT` as output path (line 150)
- Position data filter methods (lines 366, 396): Uses `CURRENT_NFL_WEEK` to filter completed weeks
- `export_teams_to_data()`: Uses `TEAM_DATA_FOLDER` (line 582)

**Refactoring:** DataExporter constructor needs: `position_json_output`, `current_nfl_week`, `team_data_folder`, `load_drafted_data`, `drafted_data_path`, `my_team_name`

### 5. `player-data-fetcher/fantasy_points_calculator.py` (Fantasy Points)

**Config imports (line 30):** `from config import NFL_SEASON`

**Usage:** `FantasyPointsExtractor.__init__(self, config=None, season: int = NFL_SEASON)` — already has constructor param, NFL_SEASON is just the default value.

**Refactoring:** Minor — change default from `NFL_SEASON` to a hardcoded year (e.g., `2025`) and remove the config import. Caller must pass `season=self.settings.season`.

### 6. `player-data-fetcher/game_data_fetcher.py` (Game Data — Internal Module)

**NOTE:** This is different from `run_game_data_fetcher.py` (covered by Feature 03).

**Config imports (line 30):** `from config import (CURRENT_NFL_WEEK, NFL_SEASON, GAME_DATA_CSV, COORDINATES_JSON, REQUEST_TIMEOUT, RATE_LIMIT_DELAY)`

**Module-level function `fetch_game_data()`** (invoked by NFLProjectionsCollector) already accepts parameters:
- `output_path` (→ replaces GAME_DATA_CSV for the caller)
- `season` (→ already passed as self.settings.season)
- `current_week` (→ already passed as self.settings.current_nfl_week)

But the `GameDataFetcher` class internally uses these config constants. Need to add `request_timeout` and `rate_limit_delay` params to `fetch_game_data()` or GameDataFetcher constructor.

`COORDINATES_JSON` is used for stadium coordinates — this is a non-CLI internal constant that can stay in config. `GAME_DATA_CSV` at line 30 may only be used as default path — need to verify.

### 7. `player-data-fetcher/config.py`

**CLI-configurable constants (to REMOVE):**
1. CURRENT_NFL_WEEK = 17 → --week
2. NFL_SEASON = 2025 → --season
3. LOAD_DRAFTED_DATA_FROM_FILE = True → --load-drafted-data
4. DRAFTED_DATA = "../data/drafted_data.csv" → --drafted-data-path
5. MY_TEAM_NAME = "Sea Sharp" → --my-team-name
6. POSITION_JSON_OUTPUT = "../data/player_data" → --position-json-output
7. TEAM_DATA_FOLDER = '../data/team_data' → --team-data-folder
8. GAME_DATA_CSV = '../data/game_data.csv' → --game-data-csv
9. ENABLE_HISTORICAL_DATA_SAVE = False → --enable-historical-save
10. ENABLE_GAME_DATA_FETCH = True → --enable-game-data
11. ESPN_PLAYER_LIMIT = 2000 → --espn-player-limit
12. LOGGING_LEVEL = 'INFO' → --log-level
13. REQUEST_TIMEOUT = 30 → --request-timeout
14. RATE_LIMIT_DELAY = 0.2 → --rate-limit-delay
15. PROGRESS_UPDATE_FREQUENCY = 10 → --progress-frequency

**Non-CLI constants (to KEEP):**
- ESPN_USER_AGENT (non-user-configurable header string)
- LOG_NAME = "player_data_fetcher"
- LOGGING_FORMAT = 'standard'
- PROGRESS_ETA_WINDOW_SIZE = 50 (internal algorithm parameter)
- COORDINATES_JSON = 'coordinates.json' (internal config file reference)

---

## Architectural Decision: Subprocess vs Direct Import

**Current:** `run_player_fetcher.py` uses subprocess + os.chdir to invoke `player_data_fetcher_main.py`

**DISCOVERY.md "After" pattern** explicitly shows:
```python
# run_player_fetcher.py
settings_dict = create_settings_dict(args)
asyncio.run(main(settings_dict))  # ← Direct call, not subprocess
```

**Implication:** Feature 01 should replace subprocess with direct Python import. This requires:
1. Adding `player-data-fetcher/` to sys.path in runner
2. Adding `settings_dict: dict | None = None` to `player_data_fetcher_main.main()`
3. Removing the `os.chdir(fetcher_dir)` from runner

**NOTE:** This is a significant architectural change. Needs checklist confirmation.

---

## Unit Test Impact

**Test files in `tests/player-data-fetcher/`:**
- `test_player_data_fetcher_main.py` (24 tests) — Tests Settings class and NFLProjectionsCollector. Settings tests will work after field additions. Collector tests mock DataExporter, no constructor signature changes needed here.
- `test_config.py` (15 tests) — **CRITICAL**: 11 tests directly reference CLI-configurable constants being removed from config.py. These 11 tests MUST be deleted as part of REQ-15. 4 tests for non-CLI constants (LOG_NAME, LOGGING_FORMAT, ESPN_USER_AGENT, PROGRESS_ETA_WINDOW_SIZE) must be kept.
- `test_player_data_exporter.py` (8 tests) — All call `DataExporter(output_dir=...)` without new params. **SAFE**: REQ-07 gives new params default values → no test changes needed.
- `test_espn_client.py` — May mock config imports; needs review during implementation
- `test_fantasy_points_calculator.py` — Tests `FantasyPointsExtractor`; since the default changes from NFL_SEASON to 2025, tests should still pass
- `test_game_data_fetcher.py` — Tests `GameDataFetcher`; since __init__ already has season/current_week params, impact minimal

**Settings class — MISSED FIELDS** (discovered during test review):
- `scoring_format: ScoringFormat = ScoringFormat.PPR` — NOT CLI-configurable, must be preserved in REQ-03
- `create_latest_files: bool = True` — NOT CLI-configurable, must be preserved in REQ-03
(These were not in the original research notes — test_player_data_fetcher_main.py revealed them)

---

## Open Questions (→ Checklist)

1. **Subprocess vs direct import** — DISCOVERY.md shows direct; needs user confirmation
2. **Keep pydantic BaseSettings or switch to simpler approach?** BaseSettings supports env var override (NFL_PROJ_* prefix) but adds complexity. Alternative: simple `create_settings_from_dict()` function that creates a Settings dataclass.
3. **E2E test mode player limit** — notes say 100 players; confirm
4. **GAME_DATA_CSV in game_data_fetcher.py** — used as module-level default in what context exactly? Need to see how GameDataFetcher uses it internally
5. **PROGRESS_ETA_WINDOW_SIZE** — confirmed non-CLI (stays in config). Just need to ensure it's not in the "remove" list.
