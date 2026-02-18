## Feature 01: refactor_player_data_fetcher — Implementation Checklist

**Purpose:** Track spec requirements during implementation (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified

**Update this file IN REAL-TIME (not batched at end)**

**Last Updated:** 2026-02-18

---

## Phase 1: Foundation — Internal modules (Tasks 1-4)

- [x] **REQ-10:** config.py — Remove 15 CLI-configurable constants (Task 1)
  - File: `player-data-fetcher/config.py`
  - Remove: CURRENT_NFL_WEEK, NFL_SEASON, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME, POSITION_JSON_OUTPUT, TEAM_DATA_FOLDER, GAME_DATA_CSV, ENABLE_HISTORICAL_DATA_SAVE, ENABLE_GAME_DATA_FETCH, LOGGING_LEVEL, PROGRESS_UPDATE_FREQUENCY, ESPN_PLAYER_LIMIT, REQUEST_TIMEOUT, RATE_LIMIT_DELAY
  - Keep: COORDINATES_JSON, ESPN_USER_AGENT, LOG_NAME, LOGGING_FORMAT, PROGRESS_ETA_WINDOW_SIZE
  - Verified: [x]

- [x] **REQ-08:** fantasy_points_calculator.py — Remove NFL_SEASON import + update default (Task 2)
  - File: `player-data-fetcher/fantasy_points_calculator.py`
  - Remove: `from config import NFL_SEASON`
  - Change: `season: int = NFL_SEASON` → `season: int = datetime.datetime.now().year`
  - Verified: [x]

- [x] **REQ-09:** game_data_fetcher.py — Refactor config imports + add request_timeout/rate_limit_delay params (Task 3)
  - File: `player-data-fetcher/game_data_fetcher.py`
  - Remove: CURRENT_NFL_WEEK, NFL_SEASON, GAME_DATA_CSV, REQUEST_TIMEOUT, RATE_LIMIT_DELAY from config import
  - Keep: COORDINATES_JSON
  - Add: `request_timeout: int = 30` and `rate_limit_delay: float = 0.2` to fetch_game_data() signature
  - Verified: [x]

- [x] **REQ-07:** player_data_exporter.py — Add constructor parameters (Task 4)
  - File: `player-data-fetcher/player_data_exporter.py`
  - Remove: config import of CLI-configurable constants
  - Add constructor params: current_nfl_week=17, position_json_output, team_data_folder, load_drafted_data=True, drafted_data_path, my_team_name='Sea Sharp'
  - Backward compat: `DataExporter(output_dir=...)` still works
  - Verified: [x]

**Phase 1 Tests:**
- [x] `pytest tests/player-data-fetcher/ -x` — all existing tests pass after Phase 1

---

## Phase 2: Core — player_data_fetcher_main.py (Tasks 5-7)

- [x] **REQ-03 + REQ-02d:** Settings @dataclass + create_settings_from_dict() (Task 5)
  - File: `player-data-fetcher/player_data_fetcher_main.py`
  - Remove: `from pydantic_settings import BaseSettings, SettingsConfigDict`
  - Add: `from dataclasses import dataclass`
  - Replace: `class Settings(BaseSettings)` → `@dataclass class Settings`
  - Add fields: espn_player_limit, position_json_output, team_data_folder, game_data_csv, enable_historical_save, enable_game_data, load_drafted_data, drafted_data_path, my_team_name, progress_frequency, log_level, e2e_test, logging_to_file
  - Update existing fields: season, current_nfl_week, request_timeout, rate_limit_delay (no longer from config)
  - Preserve: validate_settings() method, scoring_format, create_latest_files
  - Add: `create_settings_from_dict(args_dict: dict) -> Settings` function
  - Verified: [x]

- [x] **REQ-04 + REQ-05:** Remove config imports + fix bare config usage in methods (Task 6)
  - File: `player-data-fetcher/player_data_fetcher_main.py`
  - Remove from config import: NFL_SEASON, CURRENT_NFL_WEEK, REQUEST_TIMEOUT, RATE_LIMIT_DELAY, LOGGING_LEVEL, ENABLE_HISTORICAL_DATA_SAVE, ENABLE_GAME_DATA_FETCH
  - Keep in config import: LOG_NAME, LOGGING_FORMAT
  - Fix save_to_historical_data(): ENABLE_HISTORICAL_DATA_SAVE → self.settings.enable_historical_save; CURRENT_NFL_WEEK → self.settings.current_nfl_week; NFL_SEASON → self.settings.season
  - Fix fetch_game_data() method: ENABLE_GAME_DATA_FETCH → self.settings.enable_game_data; CURRENT_NFL_WEEK → self.settings.current_nfl_week; NFL_SEASON → self.settings.season
  - Fix main(): ENABLE_GAME_DATA_FETCH → settings.enable_game_data; ENABLE_HISTORICAL_DATA_SAVE → settings.enable_historical_save
  - Verified: [x]

- [x] **REQ-02a + REQ-02b + REQ-11 (graceful skip):** main() signature + E2E skip (Task 7)
  - File: `player-data-fetcher/player_data_fetcher_main.py`
  - Change: `async def main()` → `async def main(settings_dict: dict | None = None) -> None`
  - When None: run internal argparse (backward compat for direct invocation)
  - When dict: call create_settings_from_dict(settings_dict)
  - Add E2E graceful skip: if e2e_test=True AND file missing → log info + continue (no FileNotFoundError)
  - When e2e_test=False AND file missing → FileNotFoundError preserved
  - Verified: [x]

**Phase 2 Tests:**
- [x] `pytest tests/player-data-fetcher/ -x` — all existing tests pass after Phase 2

---

## Phase 3: ESPN Client (Task 8)

- [x] **REQ-06:** espn_client.py — Remove all scattered config imports (Task 8)
  - File: `player-data-fetcher/espn_client.py`
  - Top-level (line 27): Remove ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK; keep ESPN_USER_AGENT
  - Inline (lines 617, 651, 914, 981, 1068, 1469, 1878): Remove NFL_SEASON/CURRENT_NFL_WEEK imports
  - Inline (line 1068): Remove PROGRESS_UPDATE_FREQUENCY; keep PROGRESS_ETA_WINDOW_SIZE
  - Replace throughout: ESPN_PLAYER_LIMIT → self.settings.espn_player_limit; CURRENT_NFL_WEEK → self.settings.current_nfl_week; NFL_SEASON → self.settings.season; PROGRESS_UPDATE_FREQUENCY → self.settings.progress_frequency
  - Also update: FantasyPointsExtractor caller to pass season=self.settings.season explicitly
  - Verified: [x]

**Phase 3 Tests:**
- [x] `pytest tests/player-data-fetcher/ -x` — all existing tests pass after Phase 3

---

## Phase 4: Runner (Task 9)

- [x] **REQ-01 + REQ-02 + REQ-11 + REQ-12 + REQ-13 + REQ-14:** run_player_fetcher.py full refactor (Task 9)
  - File: `run_player_fetcher.py`
  - Remove: subprocess, os.chdir
  - Add: sys.path.insert for player-data-fetcher; import player_data_fetcher_main
  - Add: `parse_args(argv=None)` function (module-level, not in __main__)
  - Add: `create_settings_dict(args) -> dict` function (module-level)
  - All 17 args: --e2e-test, --log-level, --week, --season, --my-team-name, --load-drafted-data (BooleanOptionalAction), --drafted-data-path, --position-json-output, --team-data-folder, --game-data-csv, --enable-historical-save, --enable-game-data (BooleanOptionalAction), --espn-player-limit, --request-timeout, --rate-limit-delay, --progress-frequency, --enable-log-file
  - E2E override: espn_player_limit = 100 if e2e_test else args.espn_player_limit
  - __main__: args = parse_args(); settings_dict = create_settings_dict(args); asyncio.run(main(settings_dict))
  - Verified: [x]

**Phase 4 Tests:**
- [x] `pytest tests/player-data-fetcher/ -x` — all existing tests pass after Phase 4
- [x] `python run_player_fetcher.py --help` shows all 17 args

---

## Phase 5: Test Updates (Tasks 10-11)

- [x] **REQ-15:** test_config.py — Delete 11 tests (Task 10)
  - File: `tests/player-data-fetcher/test_config.py`
  - Delete: test_current_nfl_week_is_valid, test_nfl_season_is_valid, test_load_drafted_data_from_file_is_boolean, test_drafted_data_path_is_string, test_my_team_name_is_string, test_logging_level_is_valid, test_progress_update_frequency_is_positive, test_espn_player_limit_is_positive, test_request_timeout_is_positive, test_rate_limit_delay_is_non_negative, test_team_data_folder_is_valid_path
  - Keep: test_log_name_is_string, test_logging_format_is_valid, test_progress_eta_window_size_is_positive, test_espn_user_agent_is_string
  - Verified: [x]

- [x] **All REQs:** Create 87 new tests across 8 files (Task 11)
  - [x] `tests/player-data-fetcher/test_run_player_fetcher.py` (NEW — 31 tests)
  - [x] `tests/player-data-fetcher/test_settings_and_flow.py` (NEW — 19 tests)
  - [x] Extend `tests/player-data-fetcher/test_player_data_fetcher_main.py` (+11 tests)
  - [x] Extend `tests/player-data-fetcher/test_espn_client.py` (+5 tests)
  - [x] Extend `tests/player-data-fetcher/test_player_data_exporter.py` (+6 tests)
  - [x] Extend `tests/player-data-fetcher/test_fantasy_points_calculator.py` (+3 tests)
  - [x] Extend `tests/player-data-fetcher/test_game_data_fetcher.py` (+4 tests)
  - [x] Extend `tests/player-data-fetcher/test_config.py` (+4 tests)
  - Verified: [x]

**Phase 5 Tests:**
- [x] `pytest tests/player-data-fetcher/ -v` — 100% pass (all new + existing)
- [x] `pytest tests/ -x` — full test suite 100% pass

---

## Acceptance Criteria (from spec.md)

- [x] `python run_player_fetcher.py --help` displays all 17 arguments
- [ ] `python run_player_fetcher.py --week 1 --e2e-test` exits 0 in ≤180s (S7 E2E test)
- [ ] `python run_player_fetcher.py --e2e-test --log-level DEBUG` enables DEBUG logging (S7)
- [x] `python run_player_fetcher.py` (no args) behavior identical to current
- [x] `grep -r "CURRENT_NFL_WEEK\|NFL_SEASON\|ESPN_PLAYER_LIMIT" player-data-fetcher/config.py` returns empty
- [x] `grep -r "from pydantic_settings" player-data-fetcher/player_data_fetcher_main.py` returns empty
- [x] `grep -r "subprocess" run_player_fetcher.py` returns empty (docstring comment only)
- [x] `python run_player_fetcher.py --e2e-test` completes with exit 0 regardless of drafted_data.csv
- [x] `python player-data-fetcher/player_data_fetcher_main.py` (direct invocation) still works
- [x] `pytest tests/` reports 2,701+ passed, 0 failed

---

## Summary

**Total Requirements:** 15 (REQ-01 through REQ-15)
**Implemented:** 15
**Remaining:** 0

**Phase Progress:**
- Phase 1 (Foundation): 4/4 tasks ✅
- Phase 2 (Core module): 3/3 tasks ✅
- Phase 3 (ESPN client): 1/1 tasks ✅
- Phase 4 (Runner): 1/1 tasks ✅
- Phase 5 (Tests): 2/2 tasks ✅

**Last Updated:** 2026-02-18 — S6 complete, all phases done, 2701 tests passing
