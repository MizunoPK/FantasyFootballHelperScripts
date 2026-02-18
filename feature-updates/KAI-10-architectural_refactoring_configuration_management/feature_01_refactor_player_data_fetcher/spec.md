## Feature Spec: refactor_player_data_fetcher

**Status:** PENDING USER APPROVAL (S2.P1.I3 — Gate 3)
**Last Updated:** 2026-02-18

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 1 (solo) — Internal dependency injection refactoring (5 modules) + 14+ CLI args + debug/E2E modes. Sets design precedents for all other scripts.

**Key scope items:**
- Refactor 5 internal modules from direct config imports to constructor parameters: player_data_fetcher_main.py, espn_client.py, game_data_fetcher.py, fantasy_points_calculator.py, player_data_exporter.py
- Add 14+ CLI args to run_player_fetcher.py (replacing 11 constants + LOGGING_LEVEL + 3 optional args)
- Add universal args: --debug, --e2e-test, --log-level
- Remove all CLI-configurable constants from player-data-fetcher/config.py
- Implement --e2e-test mode completing in ≤180 seconds
- Implement --debug mode (DEBUG logging + reduced data scope)

### Relevant Discovery Decisions

- **Solution Approach:** Constructor parameter pattern — pass configuration via runner → main() → internal modules via settings dict/class; argparse defaults are single source of truth
- **Key Constraints:** Zero CLI constants in config.py after epic; all 2,744 existing tests must continue to pass; behavioral equivalence preserved
- **Dependencies:** None (Wave 1 solo — this feature sets the precedent)
- **Verification:** player_data_fetcher_main.py uses DIRECT imports (from config import ...), NOT importlib override

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Merge internal refactoring and argparse into single feature? | Yes — single refactor_player_data_fetcher feature | This feature covers both DI refactoring AND CLI args |
| Documentation as separate feature? | No — integrated into S7.P3 + S10 | README.md updates handled in S7.P3 for this feature |
| Team name arg naming? | --my-team-name | Consistent across player_fetcher and league_helper |

---

## Requirements

### REQ-01: CLI Arguments — run_player_fetcher.py

**Source:** Epic Request (notes file — "~14 args", Section 2: Comprehensive CLI Argument Support) + S2 research (config.py constants verified)

Add the following CLI arguments to `run_player_fetcher.py` via argparse:

**Universal arguments (all 7 scripts):**
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--debug` | flag | False | Enable debug mode (DEBUG logging + reduced data scope) |
| `--e2e-test` | flag | False | E2E test mode: completes in ≤180 seconds |
| `--log-level` | str | 'INFO' | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

**Script-specific arguments:**
| Argument | Type | Default | Source Constant Removed |
|----------|------|---------|------------------------|
| `--week` | int | 17 | CURRENT_NFL_WEEK |
| `--season` | int | 2025 | NFL_SEASON |
| `--my-team-name` | str | 'Sea Sharp' | MY_TEAM_NAME |
| `--load-drafted-data` | flag | True | LOAD_DRAFTED_DATA_FROM_FILE |
| `--drafted-data-path` | str | '../data/drafted_data.csv' | DRAFTED_DATA |
| `--position-json-output` | str | '../data/player_data' | POSITION_JSON_OUTPUT |
| `--team-data-folder` | str | '../data/team_data' | TEAM_DATA_FOLDER |
| `--game-data-csv` | str | '../data/game_data.csv' | GAME_DATA_CSV |
| `--enable-historical-save` | flag | False | ENABLE_HISTORICAL_DATA_SAVE |
| `--enable-game-data` | flag | True | ENABLE_GAME_DATA_FETCH |
| `--espn-player-limit` | int | 2000 | ESPN_PLAYER_LIMIT |
| `--request-timeout` | int | 30 | REQUEST_TIMEOUT |
| `--rate-limit-delay` | float | 0.2 | RATE_LIMIT_DELAY |
| `--progress-frequency` | int | 10 | PROGRESS_UPDATE_FREQUENCY |

**Backward-compatible arguments (preserved):**
| Argument | Type | Default | Note |
|----------|------|---------|------|
| `--enable-log-file` | flag | False | Pre-existing arg — preserved as-is |

**Total: 18 CLI arguments** (14 script-specific + 3 universal + 1 preserved)

**NOTE:** Current runner uses subprocess pattern. **RESOLVED (Q1):** Replace subprocess with direct import — `run_player_fetcher.py` adds `player-data-fetcher/` to `sys.path`, imports `player_data_fetcher_main`, and calls `asyncio.run(main(settings_dict))`. Remove `subprocess.run()` and `os.chdir()`.

---

### REQ-02: Architecture — runner → main() settings flow

**Source:** Epic Request (notes file — "Constructor Parameter Pattern" section) + DISCOVERY.md Technical Analysis

The settings flow must be:
```python
# run_player_fetcher.py
settings_dict = create_settings_dict(args)  # Build dict from parsed args
asyncio.run(player_data_fetcher_main.main(settings_dict))
```

**Sub-requirements:**
- REQ-02a: `main()` must accept `settings_dict: dict | None = None`
- REQ-02b: When `settings_dict` is None, `main()` runs its own argparse to build defaults (backward compatibility for direct `python player_data_fetcher_main.py` invocation)
- REQ-02c: `create_settings_dict(args)` in `run_player_fetcher.py` creates dict with all arg values from parsed argparse namespace
- REQ-02d: `create_settings_from_dict(args_dict)` in `player_data_fetcher_main.py` builds the Settings dataclass from the dict (see REQ-03)

**RESOLVED (Q1):** Replace subprocess with direct Python call — confirmed.

---

### REQ-03: player_data_fetcher_main.py — Settings class refactoring

**Source:** Epic Request (DI pattern) + S2 research (Settings class exists, already partially there)

**RESOLVED (Q2):** Replace `Settings(BaseSettings)` with a plain `@dataclass`. Remove `pydantic_settings` import. Add `create_settings_from_dict(args_dict: dict) -> Settings` function that builds Settings from the dict. Env var override (NFL_PROJ_*) intentionally dropped.

The `Settings` dataclass must include ALL fields:

**Fields to ADD (currently missing from Settings):**
- `espn_player_limit: int = 2000`
- `position_json_output: str = '../data/player_data'`
- `team_data_folder: str = '../data/team_data'`
- `game_data_csv: str = '../data/game_data.csv'`
- `enable_historical_save: bool = False`
- `enable_game_data: bool = True`
- `load_drafted_data: bool = True`
- `drafted_data_path: str = '../data/drafted_data.csv'`
- `my_team_name: str = 'Sea Sharp'`
- `progress_frequency: int = 10`
- `log_level: str = 'INFO'`
- `debug: bool = False`
- `e2e_test: bool = False`
- `logging_to_file: bool = False`

**Fields already present (keep, update defaults from hardcoded values not config):**
- `scoring_format: ScoringFormat` (default: ScoringFormat.PPR — NOT CLI-configurable, preserve as-is)
- `create_latest_files: bool` (default: True — NOT CLI-configurable, preserve as-is)
- `season: int` (default: 2025, NOT from config)
- `current_nfl_week: int` (default: 17, NOT from config)
- `request_timeout: int` (default: 30, NOT from config)
- `rate_limit_delay: float` (default: 0.2, NOT from config)

**`create_settings_from_dict()` function:**
```python
def create_settings_from_dict(args_dict: dict) -> Settings:
    """Build Settings dataclass from parsed CLI args dict."""
    return Settings(
        season=args_dict['season'],
        current_nfl_week=args_dict['week'],
        # ... all fields mapped from args_dict keys
    )
```

**Note on existing tests:** `test_player_data_fetcher_main.py` tests `Settings()` with keyword args and `settings.validate_settings()`. After switch to dataclass, `Settings()` still works with keyword args (dataclass default behavior). The `validate_settings()` method must be preserved on the dataclass (regular method, not a pydantic validator).

---

### REQ-04: player_data_fetcher_main.py — Remove config imports for CLI-configurable constants

**Source:** Epic Request ("Remove CLI constants from config files") + S2 research

Remove from `from config import (...)`:
- NFL_SEASON ❌ remove
- CURRENT_NFL_WEEK ❌ remove
- REQUEST_TIMEOUT ❌ remove
- RATE_LIMIT_DELAY ❌ remove
- LOGGING_LEVEL ❌ remove
- ENABLE_HISTORICAL_DATA_SAVE ❌ remove
- ENABLE_GAME_DATA_FETCH ❌ remove

Keep from config import:
- LOG_NAME ✅ keep (non-CLI internal constant)
- LOGGING_FORMAT ✅ keep (non-CLI internal constant)

---

### REQ-05: player_data_fetcher_main.py — Fix bare config usage in methods

**Source:** S2 research (discovered during code inspection)

Fix `NFLProjectionsCollector` methods that use bare config constants:

- `save_to_historical_data()`:
  - Replace `ENABLE_HISTORICAL_DATA_SAVE` → `self.settings.enable_historical_save`
  - Replace `CURRENT_NFL_WEEK` → `self.settings.current_nfl_week`
  - Replace `NFL_SEASON` → `self.settings.season`

- `fetch_game_data()`:
  - Replace `ENABLE_GAME_DATA_FETCH` → `self.settings.enable_game_data`
  - Replace `CURRENT_NFL_WEEK` → `self.settings.current_nfl_week`
  - Replace `NFL_SEASON` → `self.settings.season`

- `main()` function:
  - Replace `ENABLE_GAME_DATA_FETCH` → `settings.enable_game_data` (use settings)
  - Replace `ENABLE_HISTORICAL_DATA_SAVE` → `settings.enable_historical_save`

---

### REQ-06: espn_client.py — Remove config imports for CLI-configurable constants

**Source:** Epic Request + S2 research (10+ scattered imports found)

**Top-level import change:**
```python
# BEFORE
from config import (ESPN_USER_AGENT, ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK)

# AFTER
from config import ESPN_USER_AGENT  # Non-CLI constant stays
```

**Scattered inline imports to remove/replace:**
- All `from config import CURRENT_NFL_WEEK, NFL_SEASON` inside methods → use `self.settings.current_nfl_week` and `self.settings.season`
- All `from config import NFL_SEASON` inside methods → use `self.settings.season`
- `from config import CURRENT_NFL_WEEK` → use `self.settings.current_nfl_week`
- `from config import (PROGRESS_UPDATE_FREQUENCY, PROGRESS_ETA_WINDOW_SIZE, CURRENT_NFL_WEEK)` → use `self.settings.*` for progress_frequency and current_nfl_week; import PROGRESS_ETA_WINDOW_SIZE from config (non-CLI constant stays)
- All `ESPN_PLAYER_LIMIT` references → use `self.settings.espn_player_limit`

**Files with config imports to fix (by line):**
- Line 27 (top-level): Remove ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK
- Lines 617, 651, 914, 981, 1068: Remove inline NFL_SEASON/CURRENT_NFL_WEEK imports → use self.settings
- Line 1469: Remove PROGRESS_UPDATE_FREQUENCY from inline import; keep PROGRESS_ETA_WINDOW_SIZE (non-CLI)
- Line 1878: Remove inline CURRENT_NFL_WEEK import

---

### REQ-07: player_data_exporter.py — Refactor to constructor parameters

**Source:** Epic Request + S2 research

DataExporter constructor must accept all CLI-configurable parameters:

```python
# BEFORE
def __init__(self, output_dir: str, create_latest_files: bool = True):
    # Uses POSITION_JSON_OUTPUT, CURRENT_NFL_WEEK, TEAM_DATA_FOLDER,
    # LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME from config

# AFTER
def __init__(
    self,
    output_dir: str,
    current_nfl_week: int = 17,
    position_json_output: str = '../data/player_data',
    team_data_folder: str = '../data/team_data',
    load_drafted_data: bool = True,
    drafted_data_path: str = '../data/drafted_data.csv',
    my_team_name: str = 'Sea Sharp',
    create_latest_files: bool = True
):
```

**Note on default values:** New parameters use sensible defaults matching the old config values. This preserves backward compatibility for existing `test_player_data_exporter.py` tests that call `DataExporter(output_dir=...)` without the new params — those 8 tests remain valid without modification. The NFLProjectionsCollector passes explicit values from `self.settings`.

Remove module-level: `from config import POSITION_JSON_OUTPUT, CURRENT_NFL_WEEK, TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME`

Update `NFLProjectionsCollector.__init__` to pass these from `self.settings` when creating DataExporter.

---

### REQ-08: fantasy_points_calculator.py — Remove config default

**Source:** Epic Request + S2 research

`FantasyPointsExtractor.__init__` currently uses `season: int = NFL_SEASON` as default.

**RESOLVED (Q4):** Change default to `season: int = datetime.datetime.now().year` (self-maintaining, no hardcoded year).

Add `import datetime` if not already imported.

Remove: `from config import NFL_SEASON`

ESPNClient (the caller) must pass `season=self.settings.season` explicitly.

---

### REQ-09: game_data_fetcher.py (player-data-fetcher internal) — Refactor config usage

**Source:** Epic Request + S2 research

`from config import (CURRENT_NFL_WEEK, NFL_SEASON, GAME_DATA_CSV, COORDINATES_JSON, REQUEST_TIMEOUT, RATE_LIMIT_DELAY)` must be updated:

- Remove: CURRENT_NFL_WEEK, NFL_SEASON, GAME_DATA_CSV, REQUEST_TIMEOUT, RATE_LIMIT_DELAY
- Keep: COORDINATES_JSON (non-CLI internal config — stadium coordinates file)

The `fetch_game_data()` module-level function already accepts `output_path`, `season`, `current_week` from the caller. Add `request_timeout` and `rate_limit_delay` as parameters.

The `GameDataFetcher` class must use constructor parameters instead of config constants.

---

### REQ-10: config.py — Remove CLI-configurable constants

**Source:** Epic Request ("Zero CLI constants in config files") + S2 research (15 constants verified)

**Remove from player-data-fetcher/config.py:**
1. CURRENT_NFL_WEEK
2. NFL_SEASON
3. LOAD_DRAFTED_DATA_FROM_FILE
4. DRAFTED_DATA
5. MY_TEAM_NAME
6. POSITION_JSON_OUTPUT
7. TEAM_DATA_FOLDER
8. GAME_DATA_CSV
9. ENABLE_HISTORICAL_DATA_SAVE
10. ENABLE_GAME_DATA_FETCH
11. ESPN_PLAYER_LIMIT
12. LOGGING_LEVEL
13. REQUEST_TIMEOUT
14. RATE_LIMIT_DELAY
15. PROGRESS_UPDATE_FREQUENCY

**Keep in player-data-fetcher/config.py:**
- ESPN_USER_AGENT (non-CLI internal constant)
- LOG_NAME (non-CLI internal constant)
- LOGGING_FORMAT (non-CLI internal constant)
- PROGRESS_ETA_WINDOW_SIZE (non-CLI algorithm parameter)
- COORDINATES_JSON (non-CLI internal config reference)

---

### REQ-11: E2E Test Mode (--e2e-test)

**Source:** Epic Request (Section 3: E2E Test Modes) + EPIC_TICKET.md AC-03

When `--e2e-test` flag is set:
- Set `espn_player_limit = 100` (limit API data fetched)
- Script must complete in ≤180 seconds
- Exit code 0 on success
- No errors in output

**Drafted data behavior in E2E mode (RESOLVED Q3 — Option C):**
- If `--load-drafted-data` is True AND the drafted data file exists → load it normally
- If `--load-drafted-data` is True AND the drafted data file does NOT exist → skip loading silently (log a debug/info message, no exception)
- Outside E2E mode: missing drafted data file still raises `FileNotFoundError` as current behavior

**Precedence rule (Source: Epic Request — "Precedence rules"):**
- `--e2e-test` takes precedence for data limits over individual `--espn-player-limit` value

---

### REQ-12: Debug Mode (--debug)

**Source:** Epic Request (Section 4: Debug Mode Support)

When `--debug` flag is set:
- Set logging level to DEBUG (overrides `--log-level`)
- Set `espn_player_limit = 100` (reduce data scope)

**Precedence rule (Source: Epic Request — "Precedence rules"):**
- `--debug` forces DEBUG logging (overrides `--log-level`)
- `--e2e-test` takes precedence for data limits (not --debug)

---

### REQ-13: --log-level behavior

**Source:** Epic Request (universal argument spec)

- `--log-level` accepts: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Default: INFO
- `--debug` overrides this to DEBUG

---

### REQ-14: Backward Compatibility

**Source:** Derived requirement (zero regression requirement from EPIC_TICKET.md)

- Running `python run_player_fetcher.py` (no args) must behave identically to current behavior
- Running `python run_player_fetcher.py --enable-log-file` must preserve existing behavior
- All 2,744+ existing unit tests must pass after refactoring

---

### REQ-15: Update test_config.py — Remove tests for deleted constants

**Source:** S2 research (test_config.py directly tests CLI-configurable constants)

`tests/player-data-fetcher/test_config.py` has 15 test methods. When REQ-10 removes CLI-configurable constants from config.py, 11 of those test methods will fail. They must be deleted as part of this feature.

**Tests to DELETE** (test CLI-configurable constants being removed):
- `TestNFLConfiguration` (2 tests): `test_current_nfl_week_is_valid`, `test_nfl_season_is_valid`
- `TestDataPreservationSettings` (3 tests): `test_load_drafted_data_from_file_is_boolean`, `test_drafted_data_path_is_string`, `test_my_team_name_is_string`
- `TestLoggingConfiguration` (1 test): `test_logging_level_is_valid`
- `TestProgressTrackingConfiguration` (1 test): `test_progress_update_frequency_is_positive`
- `TestESPNAPIConfiguration` (3 tests): `test_espn_player_limit_is_positive`, `test_request_timeout_is_positive`, `test_rate_limit_delay_is_non_negative`
- `TestTeamDataConfiguration` (1 test): `test_team_data_folder_is_valid_path`

**Tests to KEEP** (test non-CLI constants that remain in config.py):
- `TestLoggingConfiguration`: `test_log_name_is_string`, `test_logging_format_is_valid`
- `TestProgressTrackingConfiguration`: `test_progress_eta_window_size_is_positive`
- `TestESPNAPIConfiguration`: `test_espn_user_agent_is_string`

---

## Acceptance Criteria

- [ ] `python run_player_fetcher.py --help` displays all 18 arguments
- [ ] `python run_player_fetcher.py --week 1 --espn-player-limit 100 --e2e-test` exits 0 in ≤180s
- [ ] `python run_player_fetcher.py --debug` enables DEBUG logging and sets espn_player_limit to 100
- [ ] `python run_player_fetcher.py` (no args) behavior identical to current
- [ ] `grep -r "CURRENT_NFL_WEEK\|NFL_SEASON\|ESPN_PLAYER_LIMIT" player-data-fetcher/config.py` returns empty
- [ ] `grep -r "from pydantic_settings" player-data-fetcher/player_data_fetcher_main.py` returns empty
- [ ] `grep -r "subprocess" run_player_fetcher.py` returns empty
- [ ] `python run_player_fetcher.py --e2e-test` completes with exit 0 regardless of whether `../data/drafted_data.csv` exists
- [ ] `python player-data-fetcher/player_data_fetcher_main.py` (direct invocation, no args) still works
- [ ] `pytest tests/` reports all 2,744+ passed, 0 failed

---

## Open Scope Questions

All checklist questions resolved. No open scope questions remain.

**Decisions made (see `checklist.md`):**
1. **Architecture:** Replace subprocess with direct import (Q1 → A)
2. **Settings class:** Switch to simple `@dataclass` (Q2 → B)
3. **E2E `--load-drafted-data`:** Use file if present, skip gracefully if not (Q3 → C)
4. **`fantasy_points_calculator.py` default:** `datetime.datetime.now().year` (Q4 → B)

---

## Files to Modify

| File | Change Type | Complexity |
|------|-------------|------------|
| `run_player_fetcher.py` | Refactor (subprocess→import, add argparse) | Medium |
| `player-data-fetcher/player_data_fetcher_main.py` | Refactor (Settings class, main() signature, fix methods) | High |
| `player-data-fetcher/espn_client.py` | Refactor (remove 10+ scattered config imports) | High |
| `player-data-fetcher/player_data_exporter.py` | Refactor (constructor params with defaults) | Medium |
| `player-data-fetcher/game_data_fetcher.py` | Refactor (constructor params, remove config) | Medium |
| `player-data-fetcher/fantasy_points_calculator.py` | Minor (remove NFL_SEASON default) | Low |
| `player-data-fetcher/config.py` | Remove 15 CLI-configurable constants | Low |
| `tests/player-data-fetcher/test_config.py` | Delete 11 tests for removed constants (keep 4) | Low |

**Total: 8 files to modify**
