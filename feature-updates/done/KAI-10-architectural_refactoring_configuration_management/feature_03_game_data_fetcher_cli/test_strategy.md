## Test Strategy: game_data_fetcher_cli

**Purpose:** Define testing approach for Feature 03 — adding CLI args to run_game_data_fetcher.py.

**Created:** 2026-02-18 (S4.I4)
**Last Updated:** 2026-02-18
**Status:** VALIDATED (Validation Loop passed — 3 consecutive clean rounds)

---

## Test Coverage Summary

**Total Tests Planned:** 42 tests
**Coverage Goal:** >90%
**Coverage Estimate:** ~95%

**Test Distribution:**
- Unit Tests: 18 tests
- Integration Tests: 10 tests
- Edge Case Tests: 9 tests
- Configuration Tests: 5 tests

---

## Traceability Matrix

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| REQ-01: Universal CLI args (--e2e-test, --log-level) | Tests 1.1–1.6 | 100% |
| REQ-02: Argparse defaults as single source of truth | Tests 2.1–2.4 | 100% |
| REQ-03: Remove config imports from runner | Tests 3.1–3.2 | 100% |
| REQ-04: Remove os.chdir() from runner | Tests 4.1–4.2 | 100% |
| REQ-05: Wire --log-level to setup_logger | Tests 5.1–5.2 | 100% |
| REQ-06: E2E Test Mode (--e2e-test) | Tests 6.1–6.5 | 100% |
| REQ-07: --log-level behavior | Tests 7.1–7.2 | 100% |
| REQ-08: Backward Compatibility | Tests 8.1–8.4 | 100% |
| REQ-09: --historical-season flag | Tests 9.1–9.4 | 100% |
| REQ-10: --request-timeout CLI arg | Tests 10.1–10.3 | 100% |

---

## Unit Tests

**Test 1.1: test_argparse_all_8_args_present**
- **Purpose:** All 8 args exist in parser
- **Setup:** parse_args([])
- **Expected:** Namespace has: season=2025, current_week=17, output=..., weeks=None, e2e_test=False, log_level='INFO', historical_season=False, request_timeout=30
- **Links to:** REQ-01, REQ-02

**Test 1.2: test_e2e_test_flag_default_false**
- **Setup:** parse_args([])
- **Expected:** args.e2e_test = False
- **Links to:** REQ-01

**Test 1.3: test_e2e_test_flag_sets_true**
- **Input:** parse_args(['--e2e-test'])
- **Expected:** args.e2e_test = True
- **Links to:** REQ-01

**Test 1.4: test_log_level_default_info**
- **Setup:** parse_args([])
- **Expected:** args.log_level = 'INFO'
- **Links to:** REQ-01, REQ-07

**Test 1.5: test_log_level_choices**
- **Input:** parse_args(['--log-level', 'VERBOSE'])
- **Expected:** SystemExit
- **Links to:** REQ-01, REQ-07

**Test 1.6: test_no_debug_flag**
- **Input:** parse_args(['--debug'])
- **Expected:** SystemExit (unrecognized)
- **Links to:** REQ-01

**Test 2.1: test_season_default_2025_from_argparse**
- **Purpose:** --season defaults to 2025 (from argparse, not config)
- **Expected:** args.season = 2025
- **Links to:** REQ-02

**Test 2.2: test_current_week_default_17_from_argparse**
- **Expected:** args.current_week = 17
- **Links to:** REQ-02

**Test 2.3: test_no_config_fallback_in_runner**
- **Purpose:** Runner no longer has 'season = args.season if args.season else NFL_SEASON' pattern
- **Setup:** Read runner source / inspect logic
- **Expected:** Simple 'season = args.season' assignment (no conditional fallback)
- **Links to:** REQ-02

**Test 2.4: test_no_historical_fallback_for_current_week**
- **Purpose:** No 'if args.season < NFL_SEASON: current_week = 18' implicit logic
- **Expected:** Implicit comparison removed; only --historical-season flag triggers week=18
- **Links to:** REQ-02, REQ-09

**Test 3.1: test_config_import_removed_from_runner**
- **Purpose:** 'from config import NFL_SEASON, CURRENT_NFL_WEEK' not in runner
- **Expected:** grep 'from config import' run_game_data_fetcher.py returns empty
- **Links to:** REQ-03

**Test 3.2: test_runner_not_importing_config_at_all**
- **Purpose:** Runner works without config.py present
- **Links to:** REQ-03

**Test 4.1: test_no_os_chdir_in_runner**
- **Expected:** grep 'os.chdir' run_game_data_fetcher.py returns empty
- **Links to:** REQ-04

**Test 4.2: test_sys_path_insert_preserved**
- **Purpose:** sys.path.insert remains for import resolution
- **Expected:** sys.path.insert(0, str(fetcher_dir)) still present in runner
- **Links to:** REQ-04

**Test 5.1: test_log_level_wired_to_setup_logger**
- **Setup:** Mock setup_logger; run with ['--log-level', 'WARNING']
- **Expected:** setup_logger called with level='WARNING'
- **Links to:** REQ-05

**Test 5.2: test_log_level_info_default_to_setup_logger**
- **Setup:** Mock setup_logger; run with no args
- **Expected:** setup_logger called with level='INFO'
- **Links to:** REQ-05

**Test 6.1: test_e2e_mode_uses_weeks_1**
- **Purpose:** --e2e-test forces weeks=[1]
- **Setup:** Mock fetch_game_data; run with ['--e2e-test']
- **Expected:** fetch_game_data called with weeks=[1]
- **Links to:** REQ-06

**Test 6.2: test_e2e_mode_log_message**
- **Purpose:** E2E mode logs info about limiting to week 1
- **Setup:** Capture logs; run with ['--e2e-test']
- **Expected:** Info log contains "week 1" or "E2E test mode"
- **Links to:** REQ-06

**Test 9.1: test_historical_season_flag_default_false**
- **Setup:** parse_args([])
- **Expected:** args.historical_season = False
- **Links to:** REQ-09

**Test 9.2: test_historical_season_flag_sets_current_week_18**
- **Purpose:** --historical-season sets current_week=18
- **Setup:** Mock fetch_game_data; run with ['--historical-season', '--season', '2024']
- **Expected:** fetch_game_data called with current_week=18
- **Links to:** REQ-09

**Test 9.3: test_historical_season_info_log**
- **Purpose:** --historical-season logs info about fetching all 18 weeks
- **Expected:** Info log contains "historical" and "18 weeks"
- **Links to:** REQ-09

**Test 10.1: test_request_timeout_default_30**
- **Setup:** parse_args([])
- **Expected:** args.request_timeout = 30
- **Links to:** REQ-10

**Test 10.2: test_request_timeout_custom_value**
- **Input:** parse_args(['--request-timeout', '60'])
- **Expected:** args.request_timeout = 60
- **Links to:** REQ-10

**Test 10.3: test_request_timeout_passed_to_fetch_game_data**
- **Setup:** Mock fetch_game_data; run with ['--request-timeout', '60']
- **Expected:** fetch_game_data called with request_timeout=60
- **Links to:** REQ-10

---

## Integration Tests

**Test I-1: test_help_displays_all_8_args**
- **Expected:** All 8 args in help output
- **Links to:** REQ-01

**Test I-2: test_no_args_defaults_match_old_config**
- **Purpose:** Default season=2025, week=17, level=INFO
- **Links to:** REQ-08

**Test I-3: test_existing_season_arg_preserved**
- **Input:** run with ['--season', '2024']
- **Expected:** fetch_game_data called with season=2024
- **Links to:** REQ-08

**Test I-4: test_existing_output_arg_preserved**
- **Input:** run with ['--output', '/tmp/game_data.csv']
- **Expected:** fetch_game_data called with output_path='/tmp/game_data.csv'
- **Links to:** REQ-08

**Test I-5: test_existing_current_week_arg_preserved**
- **Input:** run with ['--current-week', '10']
- **Expected:** current_week=10 passed to fetch_game_data
- **Links to:** REQ-08

**Test I-6: test_e2e_overrides_weeks_arg**
- **Purpose:** --e2e-test overrides explicit --weeks
- **Setup:** run with ['--e2e-test', '--weeks', '1', '2', '3']
- **Expected:** weeks=[1] (E2E takes precedence)
- **Links to:** REQ-06

**Test I-7: test_historical_season_overrides_current_week**
- **Purpose:** --historical-season overrides --current-week
- **Setup:** run with ['--historical-season', '--current-week', '10']
- **Expected:** current_week=18 (historical-season wins)
- **Links to:** REQ-09

**Test I-8: test_fetch_game_data_signature_has_request_timeout**
- **Purpose:** Cross-feature: verify F01 REQ-09 was implemented (fetch_game_data has request_timeout)
- **Setup:** inspect.signature(fetch_game_data)
- **Expected:** 'request_timeout' in signature
- **Links to:** REQ-10, F01 dependency

**Test I-9: test_no_config_import_in_runner_source**
- **Expected:** 'from config import' not found in run_game_data_fetcher.py
- **Links to:** REQ-03

**Test I-10: test_no_os_chdir_in_runner_source**
- **Expected:** 'os.chdir' not found in run_game_data_fetcher.py
- **Links to:** REQ-04

---

## Edge Case Tests

**Test E-1: test_historical_season_without_season_arg**
- **Input:** parse_args(['--historical-season'])
- **Expected:** current_week=18; season=2025 (default)
- **Links to:** REQ-09

**Test E-2: test_historical_season_with_explicit_current_week**
- **Purpose:** --historical-season wins over --current-week
- **Input:** parse_args(['--historical-season', '--current-week', '5'])
- **Expected:** current_week=18 (not 5)
- **Links to:** REQ-09

**Test E-3: test_e2e_test_and_historical_season_combined**
- **Input:** parse_args(['--e2e-test', '--historical-season'])
- **Expected:** E2E: weeks=[1]; historical: current_week=18 — both applied
- **Links to:** REQ-06, REQ-09

**Test E-4: test_request_timeout_zero**
- **Input:** parse_args(['--request-timeout', '0'])
- **Expected:** args.request_timeout = 0 (accepted, immediate timeout in production)
- **Links to:** REQ-10

**Test E-5: test_season_default_no_config_access**
- **Purpose:** Default season=2025 comes from argparse, not config import
- **Expected:** Module works even if config.py removed from Python path
- **Links to:** REQ-02, REQ-03

**Test E-6: test_no_debug_flag_in_help_output**
- **Expected:** '--debug' NOT in help
- **Links to:** REQ-01

**Test E-7: test_weeks_arg_multiple_values**
- **Input:** parse_args(['--weeks', '1', '3', '5'])
- **Expected:** args.weeks = [1, 3, 5] (nargs='*' or similar)
- **Links to:** REQ-08

**Test E-8: test_log_level_wired_replaces_hardcoded_info**
- **Purpose:** 'INFO' no longer hardcoded in setup_logger call
- **Setup:** Run with ['--log-level', 'DEBUG']; spy on setup_logger
- **Expected:** setup_logger('game_data_fetcher', 'DEBUG', ...) — not hardcoded 'INFO'
- **Links to:** REQ-05

**Test E-9: test_request_timeout_type_int_not_float**
- **Input:** parse_args(['--request-timeout', '30.5'])
- **Expected:** SystemExit (type=int, decimal not accepted)
- **Links to:** REQ-10

---

## Configuration Test Matrix

| Config Value | Default | Custom | Invalid |
|--------------|---------|--------|---------|
| season | 2025 (argparse) | Test I-3 | - |
| current_week | 17 (argparse) | Test I-5 | - |
| request_timeout | 30 (argparse) | Test 10.2 | Test E-9 |
| log_level | INFO | Test 5.1 | Test 1.5 |
| historical_season | False | Test 9.2 | - |

---

## Validation Loop Summary

**Rounds Executed:** 3
**Issues Found:** 0 per round
**Exit:** 3 consecutive clean rounds ✅

**Round 1:** All 10 requirements covered; cross-feature F01 dependency test (I-8) added ✅
**Round 2:** Added E-3 (e2e + historical combined); E-9 (request_timeout int type); Test I-7 (historical overrides current-week)
**Round 3:** Spot-checked REQ-09 (historical-season flag: 4 tests covering default, week=18, log, override ✅); REQ-04 (os.chdir removed ✅); F01 dependency documented ✅. PASSED

---

## Next Steps

**Implementation Dependency Note:** F03 runner requires F01 REQ-09 to be implemented first (fetch_game_data must accept request_timeout). Test I-8 verifies this dependency is met.

This file will be merged into implementation_plan.md during S5.P1.I1.
