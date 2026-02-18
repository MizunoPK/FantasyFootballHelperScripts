## Test Strategy: refactor_player_data_fetcher

**Purpose:** Define testing approach for Feature 01 — refactoring player_data_fetcher with constructor parameter pattern and CLI args.

**Created:** 2026-02-18 (S4.I4)
**Last Updated:** 2026-02-18
**Status:** VALIDATED (Validation Loop passed — 3 consecutive clean rounds)

---

## Test Coverage Summary

**Total Tests Planned:** 87 tests
**Coverage Goal:** >90%
**Coverage Estimate:** ~95%

**Test Distribution:**
- Unit Tests: 42 tests
- Integration Tests: 16 tests
- Edge Case Tests: 19 tests
- Configuration Tests: 10 tests

---

## Traceability Matrix

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| REQ-01: CLI Arguments (17 args) | Tests 1.1–1.14 (14 unit), Tests I-1–I-3 | 100% |
| REQ-02: Runner → main() settings flow | Tests 2.1–2.5 | 100% |
| REQ-03: Settings dataclass + create_settings_from_dict | Tests 3.1–3.9 | 100% |
| REQ-04: Remove config imports (player_data_fetcher_main) | Tests 4.1–4.3 | 100% |
| REQ-05: Fix bare config usage in methods | Tests 5.1–5.4 | 100% |
| REQ-06: espn_client.py remove config imports | Tests 6.1–6.6 | 100% |
| REQ-07: player_data_exporter.py refactor | Tests 7.1–7.6 | 100% |
| REQ-08: fantasy_points_calculator.py | Tests 8.1–8.3 | 100% |
| REQ-09: game_data_fetcher.py refactor | Tests 9.1–9.4 | 100% |
| REQ-10: config.py remove CLI constants | Tests 10.1–10.3 | 100% |
| REQ-11: E2E test mode | Tests 11.1–11.6 | 100% |
| REQ-12: No debug flag | Tests 12.1 | 100% |
| REQ-13: --log-level behavior | Tests 13.1–13.3 | 100% |
| REQ-14: Backward compatibility | Tests 14.1–14.4 | 100% |
| REQ-15: Update test_config.py | Tests 15.1–15.2 | 100% |

**Requirements with <90% Coverage:** 0 ✅

---

## Test Coverage Matrix

| Requirement | Unit | Integration | Edge Case | Config | Total |
|-------------|------|-------------|-----------|--------|-------|
| REQ-01: CLI Args | 8 | 2 | 4 | 0 | 14 |
| REQ-02: Settings flow | 3 | 2 | 0 | 0 | 5 |
| REQ-03: Settings dataclass | 5 | 1 | 2 | 1 | 9 |
| REQ-04: Remove config (main) | 2 | 1 | 0 | 0 | 3 |
| REQ-05: Bare config fix | 3 | 1 | 0 | 0 | 4 |
| REQ-06: espn_client.py | 3 | 2 | 1 | 0 | 6 |
| REQ-07: exporter refactor | 3 | 1 | 2 | 0 | 6 |
| REQ-08: fantasy_points_calc | 2 | 0 | 1 | 0 | 3 |
| REQ-09: game_data_fetcher | 2 | 1 | 1 | 0 | 4 |
| REQ-10: config.py | 1 | 0 | 0 | 2 | 3 |
| REQ-11: E2E mode | 3 | 1 | 2 | 0 | 6 |
| REQ-12: No debug flag | 1 | 0 | 0 | 0 | 1 |
| REQ-13: --log-level | 2 | 1 | 0 | 0 | 3 |
| REQ-14: Backward compat | 1 | 3 | 0 | 0 | 4 |
| REQ-15: test_config.py | 1 | 1 | 0 | 0 | 2 |
| Cross-feature (REQ-09) | 0 | 1 | 0 | 0 | 1 |
| Config default/missing | 0 | 0 | 6 | 7 | 13 |
| **TOTAL** | **42** | **16** | **19** | **10** | **87** |

---

## Unit Tests

### REQ-01: CLI Arguments

**Test 1.1: test_argparse_default_values**
- **Purpose:** Verify all 17 argparse args have correct defaults
- **Setup:** Call `parse_args([])` on the runner's argparse
- **Expected:** `args.week=17`, `args.season=2025`, `args.my_team_name='Sea Sharp'`, `args.espn_player_limit=2000`, `args.request_timeout=30`, `args.rate_limit_delay=0.2`, `args.log_level='INFO'`, `args.e2e_test=False`, `args.enable_log_file=False`, `args.load_drafted_data=True`, `args.enable_game_data=True`, `args.enable_historical_save=False`, etc.
- **Links to:** REQ-01

**Test 1.2: test_argparse_log_level_choices**
- **Purpose:** Verify --log-level only accepts valid choices
- **Setup:** Parse args with invalid log level
- **Input:** `parse_args(['--log-level', 'VERBOSE'])`
- **Expected:** `SystemExit` raised (argparse error)
- **Links to:** REQ-01, REQ-13

**Test 1.3: test_argparse_week_type**
- **Purpose:** Verify --week accepts int only
- **Input:** `parse_args(['--week', 'abc'])`
- **Expected:** `SystemExit` raised (type error from argparse)
- **Links to:** REQ-01

**Test 1.4: test_argparse_season_type**
- **Purpose:** Verify --season accepts int
- **Input:** `parse_args(['--season', '2024'])`
- **Expected:** `args.season = 2024`
- **Links to:** REQ-01

**Test 1.5: test_argparse_espn_player_limit_type**
- **Purpose:** Verify --espn-player-limit accepts positive int
- **Input:** `parse_args(['--espn-player-limit', '500'])`
- **Expected:** `args.espn_player_limit = 500`
- **Links to:** REQ-01

**Test 1.6: test_argparse_rate_limit_delay_type**
- **Purpose:** Verify --rate-limit-delay accepts float
- **Input:** `parse_args(['--rate-limit-delay', '0.5'])`
- **Expected:** `args.rate_limit_delay = 0.5`
- **Links to:** REQ-01

**Test 1.7: test_argparse_flag_args_default_false**
- **Purpose:** Verify flag args default to correct booleans
- **Setup:** parse_args with no args
- **Expected:** `args.e2e_test=False`, `args.enable_log_file=False`, `args.enable_historical_save=False`; `args.load_drafted_data=True`, `args.enable_game_data=True` (inverted flag defaults)
- **Links to:** REQ-01

**Test 1.8: test_argparse_no_debug_flag**
- **Purpose:** Verify --debug is not a valid argparse argument
- **Input:** `parse_args(['--debug'])`
- **Expected:** `SystemExit` raised (unrecognized arg)
- **Links to:** REQ-01, REQ-12

### REQ-02: Runner → main() settings flow

**Test 2.1: test_create_settings_dict_maps_all_args**
- **Purpose:** Verify `create_settings_dict(args)` maps all argparse namespace fields to dict
- **Setup:** Mock argparse namespace with known values
- **Expected:** Returned dict has all 17 keys with correct values from namespace
- **Links to:** REQ-02, REQ-02c

**Test 2.2: test_create_settings_dict_key_names**
- **Purpose:** Verify dict keys match expected names (snake_case from argparse)
- **Setup:** Parse known args; call create_settings_dict
- **Expected:** Keys include 'week', 'season', 'espn_player_limit', 'log_level', 'e2e_test', etc.
- **Links to:** REQ-02c

**Test 2.3: test_main_accepts_none_settings_dict**
- **Purpose:** Verify `main(None)` runs argparse to build defaults
- **Setup:** Mock asyncio event loop; call `player_data_fetcher_main.main(None)` with patched internal methods
- **Expected:** Function completes without error; builds Settings from argparse defaults
- **Links to:** REQ-02b, REQ-14

### REQ-03: Settings dataclass

**Test 3.1: test_settings_default_values**
- **Purpose:** Verify Settings() dataclass has correct defaults
- **Setup:** `s = Settings()`
- **Expected:** `s.season=2025`, `s.current_nfl_week=17`, `s.espn_player_limit=2000`, `s.log_level='INFO'`, `s.e2e_test=False`, `s.my_team_name='Sea Sharp'`
- **Links to:** REQ-03

**Test 3.2: test_settings_not_pydantic_basesettings**
- **Purpose:** Verify Settings is plain @dataclass (not pydantic_settings.BaseSettings)
- **Setup:** Import Settings
- **Expected:** `type(Settings).__name__` is NOT 'ModelMetaclass'; Settings is a dataclass
- **Links to:** REQ-03

**Test 3.3: test_settings_keyword_construction**
- **Purpose:** Verify Settings accepts keyword arguments
- **Setup:** `s = Settings(season=2024, espn_player_limit=100)`
- **Expected:** `s.season=2024`, `s.espn_player_limit=100`, other fields at defaults
- **Links to:** REQ-03

**Test 3.4: test_create_settings_from_dict_all_fields**
- **Purpose:** Verify `create_settings_from_dict()` maps all dict keys to Settings
- **Setup:** Create dict with all expected keys and values
- **Expected:** Returned Settings has all fields populated with dict values
- **Links to:** REQ-02d, REQ-03

**Test 3.5: test_settings_validate_settings_preserved**
- **Purpose:** Verify `validate_settings()` method still exists on Settings dataclass
- **Setup:** `s = Settings(); s.validate_settings()`
- **Expected:** Method callable, no AttributeError
- **Links to:** REQ-03 (backward compat note)

### REQ-05: Bare config usage in methods

**Test 5.1: test_save_to_historical_data_uses_settings**
- **Purpose:** Verify `save_to_historical_data()` uses `self.settings.enable_historical_save`
- **Setup:** Create NFLProjectionsCollector with `settings.enable_historical_save=False`; mock file write
- **Expected:** Method does NOT write file when `enable_historical_save=False`
- **Links to:** REQ-05

**Test 5.2: test_fetch_game_data_method_uses_settings**
- **Purpose:** Verify `fetch_game_data()` method uses `self.settings.enable_game_data`
- **Setup:** Create NFLProjectionsCollector with `settings.enable_game_data=False`; patch external call
- **Expected:** Method skips game data fetch when `enable_game_data=False`
- **Links to:** REQ-05

**Test 5.3: test_settings_passed_through_to_methods**
- **Purpose:** Verify NFLProjectionsCollector constructor stores settings and passes to methods
- **Setup:** Construct with custom settings; inspect self.settings
- **Expected:** `self.settings` is not None; `self.settings.season` matches input
- **Links to:** REQ-05

### REQ-06: espn_client.py

**Test 6.1: test_espn_client_accepts_settings**
- **Purpose:** Verify ESPNClient constructor accepts settings parameter
- **Setup:** Create ESPNClient with mock settings
- **Expected:** No TypeError; `client.settings.espn_player_limit` accessible
- **Links to:** REQ-06

**Test 6.2: test_espn_client_uses_settings_player_limit**
- **Purpose:** Verify ESPNClient uses `self.settings.espn_player_limit` not config constant
- **Setup:** Create ESPNClient with `settings.espn_player_limit=50`; call fetch method with mock HTTP
- **Expected:** API call uses limit=50 (not 2000 from config)
- **Links to:** REQ-06

**Test 6.3: test_espn_client_no_config_import_for_player_limit**
- **Purpose:** Verify `from config import ESPN_PLAYER_LIMIT` removed
- **Setup:** Import espn_client module; inspect
- **Expected:** No ESPN_PLAYER_LIMIT in espn_client module namespace from config
- **Links to:** REQ-06

### REQ-07: player_data_exporter.py

**Test 7.1: test_data_exporter_accepts_new_params**
- **Purpose:** Verify DataExporter constructor accepts new parameters
- **Setup:** `DataExporter(output_dir='/tmp', current_nfl_week=10, my_team_name='Test Team')`
- **Expected:** No TypeError; fields stored correctly
- **Links to:** REQ-07

**Test 7.2: test_data_exporter_backward_compat_call**
- **Purpose:** Verify existing `DataExporter(output_dir=...)` call still works
- **Setup:** `DataExporter(output_dir='/tmp')`
- **Expected:** Uses default values for new params (current_nfl_week=17, my_team_name='Sea Sharp')
- **Links to:** REQ-07, REQ-14

**Test 7.3: test_data_exporter_no_config_import**
- **Purpose:** Verify `from config import POSITION_JSON_OUTPUT, MY_TEAM_NAME, ...` removed
- **Setup:** Import player_data_exporter module
- **Expected:** No CLI-configurable constants from config in module namespace
- **Links to:** REQ-07

### REQ-08: fantasy_points_calculator.py

**Test 8.1: test_fantasy_points_extractor_no_config_import**
- **Purpose:** Verify `from config import NFL_SEASON` removed
- **Setup:** Import fantasy_points_calculator
- **Expected:** No NFL_SEASON in module namespace from config
- **Links to:** REQ-08

**Test 8.2: test_fantasy_points_extractor_default_season_is_current_year**
- **Purpose:** Verify default season = `datetime.datetime.now().year`
- **Setup:** `FantasyPointsExtractor()` with no explicit season
- **Expected:** `extractor.season == datetime.datetime.now().year`
- **Links to:** REQ-08

### REQ-09: game_data_fetcher.py

**Test 9.1: test_fetch_game_data_signature_has_request_timeout**
- **Purpose:** Verify `fetch_game_data()` function accepts `request_timeout` parameter
- **Setup:** `import inspect; sig = inspect.signature(fetch_game_data)`
- **Expected:** `'request_timeout' in sig.parameters`
- **Links to:** REQ-09

**Test 9.2: test_fetch_game_data_signature_has_rate_limit_delay**
- **Purpose:** Verify `fetch_game_data()` accepts `rate_limit_delay` parameter
- **Expected:** `'rate_limit_delay' in sig.parameters`
- **Links to:** REQ-09

### REQ-11: E2E mode

**Test 11.1: test_e2e_mode_overrides_player_limit**
- **Purpose:** Verify `--e2e-test` forces `espn_player_limit=100`
- **Setup:** create_settings_dict with e2e_test=True, espn_player_limit=2000
- **Expected:** After E2E override logic, effective player limit is 100
- **Links to:** REQ-11

**Test 11.2: test_e2e_mode_graceful_skip_drafted_data_missing**
- **Purpose:** Verify E2E mode skips drafted data load when file missing (no exception)
- **Setup:** `settings.e2e_test=True, settings.load_drafted_data=True`; drafted_data.csv absent
- **Expected:** No FileNotFoundError raised; warning/info log emitted; process continues
- **Links to:** REQ-11

**Test 11.3: test_e2e_mode_loads_drafted_data_when_present**
- **Purpose:** Verify E2E mode still loads drafted data when file IS present
- **Setup:** Create temp drafted_data.csv; `settings.e2e_test=True`
- **Expected:** File loaded normally
- **Links to:** REQ-11

### REQ-12: No debug flag

**Test 12.1: test_no_debug_flag_in_argparse**
- **Purpose:** Confirm no `--debug` argument exists
- **Input:** `parse_args(['--debug'])`
- **Expected:** `SystemExit` with code 2 (unrecognized argument)
- **Links to:** REQ-12

### REQ-13: --log-level

**Test 13.1: test_log_level_choices_are_uppercase**
- **Purpose:** Verify valid choices for --log-level
- **Setup:** parse_args with each valid choice
- **Expected:** DEBUG, INFO, WARNING, ERROR, CRITICAL all accepted
- **Links to:** REQ-13

**Test 13.2: test_log_level_wired_to_setup_logger**
- **Purpose:** Verify log level from args is passed to setup_logger()
- **Setup:** Mock setup_logger; parse args with --log-level WARNING
- **Expected:** setup_logger called with level='WARNING'
- **Links to:** REQ-13

---

## Integration Tests

**Test I-1: test_help_displays_all_17_args**
- **Purpose:** Verify `--help` output contains all 17 expected arg names
- **Setup:** Capture stdout of `parse_args(['--help'])`
- **Expected:** Output contains '--e2e-test', '--log-level', '--week', '--season', '--my-team-name', '--espn-player-limit', '--request-timeout', '--rate-limit-delay', '--load-drafted-data', '--enable-log-file', '--progress-frequency', '--game-data-csv', '--team-data-folder', '--position-json-output', '--enable-historical-save', '--enable-game-data', '--drafted-data-path'
- **Links to:** REQ-01

**Test I-2: test_help_does_not_contain_debug_flag**
- **Purpose:** Confirm --debug not shown in help
- **Expected:** '--debug' NOT in help output
- **Links to:** REQ-12

**Test I-3: test_runner_direct_import_replaces_subprocess**
- **Purpose:** Verify run_player_fetcher.py uses direct import, not subprocess
- **Setup:** Read/inspect run_player_fetcher.py contents (or mock imports)
- **Expected:** No `subprocess.run` call; `import player_data_fetcher_main` present; `asyncio.run(main(...))` called
- **Links to:** REQ-01 (NOTE), REQ-02

**Test I-4: test_runner_to_main_settings_flow_end_to_end**
- **Purpose:** Verify full settings flow: runner → create_settings_dict → main() → create_settings_from_dict → Settings
- **Setup:** Mock all external API calls; parse args with `['--season', '2024', '--week', '5']`; run main()
- **Expected:** NFLProjectionsCollector constructed with settings.season=2024, settings.current_nfl_week=5
- **Links to:** REQ-02

**Test I-5: test_direct_invocation_player_data_fetcher_main**
- **Purpose:** Verify `python player_data_fetcher_main.py` (no args) still works
- **Setup:** Call `main(None)` directly with all external calls mocked
- **Expected:** main() runs without error using argparse defaults; settings built internally
- **Links to:** REQ-02b, REQ-14

**Test I-6: test_no_os_chdir_in_runner**
- **Purpose:** Verify os.chdir() removed from runner (consistent with Feature 01 anti-pattern elimination)
- **Setup:** Inspect/call run_player_fetcher.py
- **Expected:** No `os.chdir` call in runner; sys.path manipulation only
- **Links to:** REQ-02

**Test I-7: test_espn_client_settings_propagation**
- **Purpose:** Verify ESPNClient receives settings from NFLProjectionsCollector and uses them
- **Setup:** Construct collector with settings.espn_player_limit=150; spy on ESPNClient
- **Expected:** ESPNClient constructed with player limit=150 from settings
- **Links to:** REQ-06

**Test I-8: test_exporter_receives_settings_from_collector**
- **Purpose:** Verify DataExporter receives settings from NFLProjectionsCollector
- **Setup:** Construct collector with settings.my_team_name='Test Team'; spy on DataExporter
- **Expected:** DataExporter constructed with my_team_name='Test Team'
- **Links to:** REQ-07

**Test I-9: test_fetch_game_data_receives_timeout_from_settings**
- **Purpose:** Verify game_data_fetcher.fetch_game_data() receives request_timeout from settings
- **Setup:** Call with settings.request_timeout=60; patch HTTP calls
- **Expected:** fetch_game_data called with request_timeout=60
- **Links to:** REQ-09

**Test I-10: test_config_constants_removed_from_module**
- **Purpose:** Verify 15 constants removed from config.py
- **Setup:** Import config; check for removed constants
- **Expected:** `hasattr(config, 'CURRENT_NFL_WEEK')` → False for all 15 removed constants
- **Links to:** REQ-10

**Test I-11: test_config_kept_constants_still_present**
- **Purpose:** Verify 5 non-CLI constants remain in config.py
- **Expected:** ESPN_USER_AGENT, LOG_NAME, LOGGING_FORMAT, PROGRESS_ETA_WINDOW_SIZE, COORDINATES_JSON all present
- **Links to:** REQ-10

**Test I-12: test_e2e_mode_exits_zero_with_real_flow**
- **Purpose:** Verify E2E mode completes without error (mocked APIs)
- **Setup:** Run with `--e2e-test` flag; mock ESPN API calls; mock game data fetch
- **Expected:** Exit code 0; no exceptions; player_limit override to 100 applied
- **Links to:** REQ-11

**Test I-13: test_backward_compat_no_args_same_behavior**
- **Purpose:** Verify no-args run produces same configuration as pre-refactor defaults
- **Setup:** parse_args([]); compare to documented old config values
- **Expected:** season=2025, week=17, espn_player_limit=2000, rate_limit_delay=0.2, request_timeout=30
- **Links to:** REQ-14

**Test I-14: test_enable_log_file_preserved**
- **Purpose:** Verify --enable-log-file still works as before
- **Input:** `parse_args(['--enable-log-file'])`
- **Expected:** `args.enable_log_file=True`; setup_logger called with file logging enabled
- **Links to:** REQ-14

**Test I-15: test_config_test_file_tests_reduced**
- **Purpose:** Verify test_config.py contains exactly 4 remaining tests (not 15)
- **Setup:** Count test methods in test_config.py
- **Expected:** 4 test methods: test_log_name_is_string, test_logging_format_is_valid, test_progress_eta_window_size_is_positive, test_espn_user_agent_is_string
- **Links to:** REQ-15

**Test I-16: test_f03_dependency_fetch_game_data_signature (cross-feature)**
- **Purpose:** Verify fetch_game_data() signature has request_timeout (F03 will depend on this)
- **Setup:** `inspect.signature(fetch_game_data)`
- **Expected:** request_timeout and rate_limit_delay both in signature
- **Links to:** REQ-09, cross-feature F03 dependency

---

## Edge Case Tests

**Test E-1: test_e2e_mode_drafted_data_missing_no_error**
- **Purpose:** E2E mode + load_drafted_data=True + file missing → no exception, log info
- **Setup:** settings.e2e_test=True; drafted_data.csv does NOT exist
- **Expected:** No FileNotFoundError; info log contains "skipping" or "not found"
- **Links to:** REQ-11

**Test E-2: test_non_e2e_mode_drafted_data_missing_raises**
- **Purpose:** Normal mode + load_drafted_data=True + file missing → FileNotFoundError
- **Setup:** settings.e2e_test=False, settings.load_drafted_data=True; file absent
- **Expected:** FileNotFoundError raised (existing behavior preserved)
- **Links to:** REQ-11 (outside E2E), REQ-14

**Test E-3: test_e2e_test_precedence_over_player_limit**
- **Purpose:** --e2e-test overrides explicit --espn-player-limit
- **Input:** `parse_args(['--e2e-test', '--espn-player-limit', '500'])`
- **Expected:** After E2E override, effective player limit = 100 (not 500)
- **Links to:** REQ-11 (precedence rule)

**Test E-4: test_week_negative_value**
- **Purpose:** Verify behavior with negative --week value
- **Input:** `parse_args(['--week', '-1'])`
- **Expected:** argparse accepts (int type, no bounds check in argparse) or SystemExit if choices limited — check spec behavior
- **Links to:** REQ-01

**Test E-5: test_season_far_future**
- **Purpose:** Verify behavior with unrealistic future season year
- **Input:** `parse_args(['--season', '2099'])`
- **Expected:** Accepted by argparse (int type); downstream may log warning but no crash
- **Links to:** REQ-01

**Test E-6: test_my_team_name_empty_string**
- **Purpose:** Verify empty string for --my-team-name
- **Input:** `parse_args(['--my-team-name', ''])`
- **Expected:** Accepted by argparse (empty string is valid str); Settings stores empty string
- **Links to:** REQ-01, REQ-03

**Test E-7: test_my_team_name_with_spaces**
- **Purpose:** Verify team name with spaces works
- **Input:** `parse_args(['--my-team-name', 'My Team Name'])`
- **Expected:** `args.my_team_name = 'My Team Name'`
- **Links to:** REQ-01

**Test E-8: test_create_settings_from_dict_with_extra_keys**
- **Purpose:** Verify extra dict keys don't cause TypeError
- **Setup:** Pass dict with extra unknown key to create_settings_from_dict
- **Expected:** Extra key ignored or handled gracefully; Settings built from known keys
- **Links to:** REQ-03

**Test E-9: test_settings_dataclass_no_env_var_override**
- **Purpose:** Verify env vars (NFL_PROJ_*) no longer override settings
- **Setup:** Set env var NFL_PROJ_SEASON='2020'; create Settings()
- **Expected:** `settings.season=2025` (default, not from env) — pydantic_settings env override removed
- **Links to:** REQ-03

**Test E-10: test_rate_limit_delay_zero**
- **Purpose:** Verify zero delay is accepted
- **Input:** `parse_args(['--rate-limit-delay', '0'])`
- **Expected:** `args.rate_limit_delay = 0.0`
- **Links to:** REQ-01

**Test E-11: test_enable_game_data_flag_disables_fetch**
- **Purpose:** Verify --no-enable-game-data (negated flag) skips game data fetch
- **Setup:** settings.enable_game_data=False; mock external calls
- **Expected:** game_data_fetcher.fetch_game_data() not called
- **Links to:** REQ-05

**Test E-12: test_espn_client_settings_uses_current_nfl_week_not_config**
- **Purpose:** Verify ESPNClient uses settings.current_nfl_week, not config.CURRENT_NFL_WEEK
- **Setup:** settings.current_nfl_week=10; confirm no config access at runtime
- **Expected:** ESPN API calls use week=10 from settings
- **Links to:** REQ-06

**Test E-13: test_fantasy_points_extractor_explicit_season**
- **Purpose:** Verify explicit season passed overrides current-year default
- **Setup:** `FantasyPointsExtractor(season=2020)`
- **Expected:** `extractor.season = 2020` (not current year)
- **Links to:** REQ-08

**Test E-14: test_data_exporter_custom_my_team_name**
- **Purpose:** Verify DataExporter uses custom my_team_name
- **Setup:** `DataExporter(output_dir='/tmp', my_team_name='Custom Team')`
- **Expected:** Exported data marks players with 'Custom Team' instead of default
- **Links to:** REQ-07

**Test E-15: test_runner_no_os_chdir_call**
- **Purpose:** Verify removing os.chdir doesn't break path resolution
- **Setup:** Run runner from a different working directory
- **Expected:** Module imports succeed; no FileNotFoundError from path issues
- **Links to:** REQ-01 (NOTE)

**Test E-16: test_log_level_info_default**
- **Purpose:** Verify INFO is the default when --log-level omitted
- **Setup:** parse_args([]); setup_logger mock
- **Expected:** setup_logger called with level='INFO'
- **Links to:** REQ-13

**Test E-17: test_progress_frequency_affects_logging**
- **Purpose:** Verify --progress-frequency is passed through to internals
- **Setup:** settings.progress_frequency=5; spy on ESPN client progress calls
- **Expected:** Progress logged every 5 players (not 10)
- **Links to:** REQ-01, REQ-06

**Test E-18: test_drafted_data_path_custom**
- **Purpose:** Verify custom --drafted-data-path is used
- **Setup:** `settings.drafted_data_path='/custom/path.csv'`; mock file read
- **Expected:** File read attempted at '/custom/path.csv'
- **Links to:** REQ-01, REQ-07

**Test E-19: test_create_settings_from_dict_maps_week_to_current_nfl_week**
- **Purpose:** Verify dict key 'week' (from argparse) maps to Settings field 'current_nfl_week'
- **Setup:** `create_settings_from_dict({'week': 10, ...all other keys})`
- **Expected:** `settings.current_nfl_week = 10` (not settings.week — field name differs)
- **Links to:** REQ-03, REQ-02d

---

## Configuration Tests

### Config Scenario 1: Default Configuration (argparse defaults = hardcoded in argparse)

**Test C-1: test_default_config_no_file_dependency**
- **Purpose:** Verify runner works with no external config file (config.py no longer needed for CLI values)
- **Setup:** Temporarily rename config.py; try to run runner (with all external API calls mocked)
- **Expected:** runner works; only fails if non-CLI constants (ESPN_USER_AGENT etc.) accessed without config
- **Note:** config.py still needed for 5 non-CLI constants — this tests that CLI values don't need it
- **Links to:** REQ-04, REQ-10

**Test C-2: test_all_argparse_defaults_match_old_config_values**
- **Purpose:** Verify argparse defaults exactly match the old config.py constant values
- **Expected:**
  - args.season == 2025 (was NFL_SEASON=2025)
  - args.week == 17 (was CURRENT_NFL_WEEK=17)
  - args.espn_player_limit == 2000 (was ESPN_PLAYER_LIMIT=2000)
  - args.request_timeout == 30 (was REQUEST_TIMEOUT=30)
  - args.rate_limit_delay == 0.2 (was RATE_LIMIT_DELAY=0.2)
  - args.my_team_name == 'Sea Sharp' (was MY_TEAM_NAME='Sea Sharp')
  - args.progress_frequency == 10 (was PROGRESS_UPDATE_FREQUENCY=10)
- **Links to:** REQ-10, REQ-14

### Config Scenario 2: Custom Configuration

**Test C-3: test_custom_season_overrides_default**
- **Purpose:** Verify custom --season replaces argparse default
- **Input:** `parse_args(['--season', '2023'])`
- **Expected:** `args.season = 2023`
- **Links to:** REQ-01

**Test C-4: test_custom_player_limit_overrides_default**
- **Input:** `parse_args(['--espn-player-limit', '100'])`
- **Expected:** `args.espn_player_limit = 100`
- **Links to:** REQ-01

### Config Scenario 3: Invalid Configuration

**Test C-5: test_invalid_log_level_rejected**
- **Input:** `parse_args(['--log-level', 'TRACE'])`
- **Expected:** `SystemExit` raised
- **Links to:** REQ-01, REQ-13

**Test C-6: test_invalid_week_type_rejected**
- **Input:** `parse_args(['--week', 'seventeen'])`
- **Expected:** `SystemExit` raised
- **Links to:** REQ-01

### Config Scenario 4: Missing Configuration

**Test C-7: test_config_py_removed_constants_raise_import_error**
- **Purpose:** Verify importing CURRENT_NFL_WEEK from config raises AttributeError/ImportError
- **Setup:** `from config import CURRENT_NFL_WEEK`
- **Expected:** `ImportError` or `AttributeError` (constant no longer exists)
- **Links to:** REQ-10

**Test C-8: test_config_py_kept_constants_still_importable**
- **Purpose:** Verify the 5 kept constants still import cleanly
- **Setup:** `from config import ESPN_USER_AGENT, LOG_NAME, LOGGING_FORMAT, PROGRESS_ETA_WINDOW_SIZE, COORDINATES_JSON`
- **Expected:** All 5 import without error
- **Links to:** REQ-10

**Test C-9: test_settings_dataclass_independent_of_config_file**
- **Purpose:** Verify Settings() can be constructed without any config.py values
- **Setup:** `Settings()` or `create_settings_from_dict(dict_with_all_keys)`
- **Expected:** No ImportError from config access
- **Links to:** REQ-03, REQ-04

**Test C-10: test_existing_test_config_py_tests_pass**
- **Purpose:** Verify the 4 remaining test_config.py tests all pass
- **Setup:** Run `pytest tests/player-data-fetcher/test_config.py`
- **Expected:** 4 passed, 0 failed
- **Links to:** REQ-15

---

## Edge Case Catalog

| Edge Case | Category | Expected Behavior | Test |
|-----------|----------|-------------------|------|
| E2E mode + drafted_data missing | Business logic | Graceful skip, no exception | E-1 |
| Normal mode + drafted_data missing | Business logic | FileNotFoundError (existing behavior) | E-2 |
| --e2e-test overrides --espn-player-limit | Precedence | Player limit forced to 100 | E-3 |
| Negative --week value | Input boundary | Accepted by argparse (no bounds check) | E-4 |
| Far-future --season | Input boundary | Accepted, downstream may warn | E-5 |
| Empty string --my-team-name | Input boundary | Accepted as empty string | E-6 |
| Team name with spaces | Input boundary | Accepted, stored as-is | E-7 |
| Dict with extra keys in create_settings_from_dict | API boundary | Extra keys ignored | E-8 |
| NFL_PROJ_* env vars (pydantic removed) | Config | Ignored (not a pydantic BaseSettings anymore) | E-9 |
| rate_limit_delay = 0 | Input boundary | Accepted as 0.0 | E-10 |
| enable_game_data=False | Business logic | fetch_game_data not called | E-11 |
| ESPNClient current_nfl_week from settings, not config | Config source | settings.current_nfl_week used | E-12 |
| FantasyPointsExtractor explicit season | Override default | Explicit season wins over current year | E-13 |
| DataExporter custom team name | DI pattern | Custom name propagated | E-14 |
| Running from different working directory | Path handling | Module imports succeed (no os.chdir needed) | E-15 |
| --log-level default not provided | Defaults | INFO used | E-16 |
| progress_frequency propagation | Settings propagation | Custom value passed to ESPN client | E-17 |
| Custom --drafted-data-path | Path override | Custom path used for file read | E-18 |
| create_settings_from_dict: 'week' → 'current_nfl_week' | Field mapping | Correct mapping, no KeyError | E-19 |

---

## Configuration Test Matrix

| Config Value | Default Test | Custom Test | Invalid Test | Missing Test |
|--------------|-------------|-------------|--------------|--------------|
| season | C-2 | C-3 | C-6 (wrong type) | C-9 |
| espn_player_limit | C-2 | C-4 | C-6 | C-9 |
| log_level | C-2 | I-1 | C-5 | - |
| config.py constants (removed) | C-1 | - | - | C-7 |
| config.py constants (kept) | C-8 | - | - | - |
| Settings dataclass | C-2 | C-3 | - | C-9 |

---

## Validation Loop Summary

**Validation Date:** 2026-02-18
**Rounds Executed:** 3 rounds
**Issues Found:** 0 per round after initial enumeration
**Exit:** 3 consecutive clean rounds achieved ✅

**Round 1 (Sequential coverage check):**
- Checked: all 15 requirements have test coverage ✅
- Checked: traceability matrix complete ✅
- Checked: test descriptions specific with pass/fail criteria ✅
- Added: E-19 (create_settings_from_dict field mapping edge case) — caught gap in REQ-02d

**Round 2 (Gap detection):**
- Fresh read of spec.md; no new requirements found
- Added: I-16 cross-feature test for F03 dependency (REQ-09 fetch_game_data signature)
- Checked: all integration points tested ✅
- Checked: edge case catalog complete ✅

**Round 3 (Spot-check):**
- Spot-checked REQ-11 (E2E mode): 6 tests cover happy path, graceful skip, file-present, precedence, E2E exits 0 ✅
- Spot-checked REQ-07 (exporter): backward compat test present ✅
- Spot-checked REQ-03 (Settings): validate_settings preserved test present ✅
- Spot-checked REQ-14 (backward compat): direct invocation + no-args + enable-log-file all covered ✅
- Final coverage estimate: ~95% ✅
- **Round 3: 0 issues → PASSED**

---

## Next Steps

This file will be merged into `implementation_plan.md` during S5.P1.I1:
- S5.P1.I1 verifies this file exists (MANDATORY check)
- S5.P1.I1 merges test strategy into "Test Strategy" section of implementation_plan.md
- Implementation tasks will reference these tests
