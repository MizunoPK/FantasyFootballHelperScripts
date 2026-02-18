## Test Strategy: schedule_fetcher_cli

**Purpose:** Define testing approach for Feature 02 — adding CLI args to run_schedule_fetcher.py.

**Created:** 2026-02-18 (S4.I4)
**Last Updated:** 2026-02-18
**Status:** VALIDATED (Validation Loop passed — 3 consecutive clean rounds)

---

## Test Coverage Summary

**Total Tests Planned:** 38 tests
**Coverage Goal:** >90%
**Coverage Estimate:** ~95%

**Test Distribution:**
- Unit Tests: 18 tests
- Integration Tests: 10 tests
- Edge Case Tests: 7 tests
- Configuration Tests: 3 tests

---

## Traceability Matrix

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| REQ-01: CLI Arguments (5 args) | Tests 1.1–1.10 | 100% |
| REQ-02: Remove NFL_SEASON constant | Tests 2.1–2.3 | 100% |
| REQ-03: Architecture / settings flow | Tests 3.1–3.3 | 100% |
| REQ-04: E2E Test Mode | Tests 4.1–4.5 | 100% |
| REQ-05: --log-level behavior | Tests 5.1–5.3 | 100% |
| REQ-06: Backward Compatibility | Tests 6.1–6.4 | 100% |
| REQ-07: Update tests | Tests 7.1–7.2 | 100% |

---

## Unit Tests

**Test 1.1: test_argparse_default_values**
- **Purpose:** Verify all 5 args have correct defaults
- **Setup:** parse_args([])
- **Expected:** season=2025, output_path='data/season_schedule.csv', e2e_test=False, log_level='INFO', enable_log_file=False
- **Links to:** REQ-01

**Test 1.2: test_argparse_log_level_choices**
- **Purpose:** Verify --log-level accepts only valid choices (uppercase)
- **Input:** parse_args(['--log-level', 'VERBOSE'])
- **Expected:** SystemExit raised
- **Links to:** REQ-01, REQ-05

**Test 1.3: test_argparse_season_type**
- **Purpose:** Verify --season accepts int
- **Input:** parse_args(['--season', '2024'])
- **Expected:** args.season = 2024
- **Links to:** REQ-01

**Test 1.4: test_argparse_season_wrong_type**
- **Input:** parse_args(['--season', 'abc'])
- **Expected:** SystemExit raised
- **Links to:** REQ-01

**Test 1.5: test_argparse_output_path_accepts_string**
- **Input:** parse_args(['--output-path', '/tmp/schedule.csv'])
- **Expected:** args.output_path = '/tmp/schedule.csv'
- **Links to:** REQ-01

**Test 1.6: test_argparse_e2e_test_flag_default_false**
- **Setup:** parse_args([])
- **Expected:** args.e2e_test = False
- **Links to:** REQ-01, REQ-04

**Test 1.7: test_argparse_e2e_test_flag_sets_true**
- **Input:** parse_args(['--e2e-test'])
- **Expected:** args.e2e_test = True
- **Links to:** REQ-01, REQ-04

**Test 1.8: test_argparse_no_debug_flag**
- **Input:** parse_args(['--debug'])
- **Expected:** SystemExit raised
- **Links to:** REQ-01 (design correction — no --debug)

**Test 1.9: test_argparse_enable_log_file_preserved**
- **Input:** parse_args(['--enable-log-file'])
- **Expected:** args.enable_log_file = True
- **Links to:** REQ-01, REQ-06

**Test 1.10: test_argparse_help_contains_all_5_args**
- **Purpose:** Help output mentions all 5 arg names
- **Expected:** '--season', '--output-path', '--e2e-test', '--log-level', '--enable-log-file' all in help
- **Links to:** REQ-01

**Test 2.1: test_nfl_season_constant_removed_from_module**
- **Purpose:** NFL_SEASON module-level constant no longer present in runner
- **Setup:** Import/inspect run_schedule_fetcher module
- **Expected:** No module-level NFL_SEASON attribute
- **Links to:** REQ-02

**Test 2.2: test_season_from_args_passed_to_fetcher**
- **Purpose:** args.season passed to fetch_full_schedule (not hardcoded constant)
- **Setup:** Mock fetch_full_schedule; parse args with --season 2024
- **Expected:** fetch_full_schedule called with season=2024
- **Links to:** REQ-02

**Test 2.3: test_logger_uses_season_from_args**
- **Purpose:** Log messages use args.season not NFL_SEASON constant
- **Setup:** Capture log output with season=2023
- **Expected:** Log contains '2023', not hardcoded '2025'
- **Links to:** REQ-02

**Test 3.1: test_max_weeks_1_in_e2e_mode**
- **Purpose:** Verify E2E mode passes max_weeks=1 to fetch_full_schedule
- **Setup:** Mock fetch_full_schedule; parse args with ['--e2e-test']
- **Expected:** fetch_full_schedule called with max_weeks=1
- **Links to:** REQ-03, REQ-04

**Test 3.2: test_max_weeks_18_in_normal_mode**
- **Purpose:** Verify normal mode passes max_weeks=18
- **Setup:** Mock fetch_full_schedule; parse args with []
- **Expected:** fetch_full_schedule called with max_weeks=18
- **Links to:** REQ-03

**Test 3.3: test_fetch_full_schedule_accepts_max_weeks_param**
- **Purpose:** Verify ScheduleFetcher.fetch_full_schedule has max_weeks parameter
- **Setup:** import inspect; inspect.signature(ScheduleFetcher.fetch_full_schedule)
- **Expected:** 'max_weeks' in signature
- **Links to:** REQ-03, REQ-04

**Test 4.1: test_e2e_mode_uses_max_weeks_1**
- Already covered by Test 3.1
- **Links to:** REQ-04

**Test 4.2: test_e2e_mode_log_level_wired**
- **Purpose:** --log-level wired to setup_logger
- **Setup:** Mock setup_logger; parse_args with ['--log-level', 'WARNING']
- **Expected:** setup_logger called with level='WARNING'
- **Links to:** REQ-05

**Test 5.1: test_log_level_default_is_info**
- **Setup:** parse_args([])
- **Expected:** args.log_level = 'INFO'
- **Links to:** REQ-05

**Test 5.2: test_log_level_valid_choices_accepted**
- **Purpose:** All 5 valid levels accepted
- **Input:** Each of DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Expected:** All accepted without error
- **Links to:** REQ-05

**Test 5.3: test_log_level_wired_to_setup_logger**
- **Setup:** Mock setup_logger; args.log_level='DEBUG'
- **Expected:** setup_logger called with 'DEBUG'
- **Links to:** REQ-05

---

## Integration Tests

**Test I-1: test_help_displays_all_5_args**
- **Purpose:** Full help output check
- **Expected:** All 5 arg names present
- **Links to:** REQ-01

**Test I-2: test_no_args_behavior_matches_current**
- **Purpose:** No-args run uses season=2025, output='data/season_schedule.csv', INFO logging
- **Setup:** Mock fetch_full_schedule + setup_logger; run with []
- **Expected:** fetch called with season=2025; logger called with level='INFO'
- **Links to:** REQ-06

**Test I-3: test_enable_log_file_preserved**
- **Setup:** parse_args(['--enable-log-file'])
- **Expected:** enable_log_file=True; setup_logger called with log_to_file=True
- **Links to:** REQ-06

**Test I-4: test_e2e_mode_exits_zero_with_mocked_api**
- **Purpose:** E2E run exits 0 with mocked ScheduleFetcher
- **Setup:** Mock all external calls; run with ['--e2e-test']
- **Expected:** exit code 0; no exceptions
- **Links to:** REQ-04

**Test I-5: test_custom_output_path_passed_to_fetcher**
- **Setup:** run with ['--output-path', '/tmp/test.csv']
- **Expected:** ScheduleFetcher constructed with output_path=/tmp/test.csv
- **Links to:** REQ-01

**Test I-6: test_custom_season_passed_to_fetch_full_schedule**
- **Setup:** run with ['--season', '2023']
- **Expected:** fetch_full_schedule called with 2023
- **Links to:** REQ-01, REQ-02

**Test I-7: test_e2e_debug_combo**
- **Purpose:** --e2e-test --log-level DEBUG produces debug output
- **Setup:** Mock; run with ['--e2e-test', '--log-level', 'DEBUG']
- **Expected:** setup_logger called with 'DEBUG'; max_weeks=1
- **Links to:** REQ-04, REQ-05

**Test I-8: test_existing_15_tests_still_pass**
- **Purpose:** Regression check — existing test_run_schedule_fetcher.py tests preserved
- **Expected:** All 15 existing tests pass
- **Links to:** REQ-07

**Test I-9: test_new_arg_tests_cover_season_output_e2e_loglevel**
- **Purpose:** New test file tests cover all 4 new/modified args
- **Expected:** Tests for --season, --output-path, --e2e-test, --log-level present
- **Links to:** REQ-07

**Test I-10: test_no_nfl_season_constant_in_runner_source**
- **Purpose:** Static check: NFL_SEASON not found in runner
- **Expected:** grep 'NFL_SEASON' run_schedule_fetcher.py returns empty
- **Links to:** REQ-02

---

## Edge Case Tests

**Test E-1: test_e2e_test_overrides_explicit_max_weeks_if_provided**
- **Purpose:** --e2e-test forces max_weeks=1 regardless of other args
- **Links to:** REQ-04

**Test E-2: test_output_path_with_spaces_in_path**
- **Input:** parse_args(['--output-path', '/path with spaces/out.csv'])
- **Expected:** Accepted, stored as-is
- **Links to:** REQ-01

**Test E-3: test_season_very_old_year**
- **Input:** parse_args(['--season', '1990'])
- **Expected:** Accepted by argparse
- **Links to:** REQ-01

**Test E-4: test_season_future_year**
- **Input:** parse_args(['--season', '2030'])
- **Expected:** Accepted by argparse
- **Links to:** REQ-01

**Test E-5: test_log_level_case_sensitive_choices**
- **Input:** parse_args(['--log-level', 'debug'])  # lowercase
- **Expected:** SystemExit (choices are uppercase, no str.upper normalization on F02)
- **Links to:** REQ-05

**Test E-6: test_e2e_mode_with_custom_season**
- **Input:** parse_args(['--e2e-test', '--season', '2023'])
- **Expected:** E2E mode AND season=2023 both applied
- **Links to:** REQ-04

**Test E-7: test_no_debug_flag_in_help**
- **Purpose:** '--debug' not in help output
- **Expected:** '--debug' NOT found in help text
- **Links to:** REQ-01

---

## Configuration Tests

**Test C-1: test_default_config_season_matches_old_constant**
- **Purpose:** Default season=2025 matches old NFL_SEASON=2025 constant
- **Expected:** args.season = 2025 (same value, now from argparse default not constant)
- **Links to:** REQ-02, REQ-06

**Test C-2: test_invalid_log_level_rejected**
- **Input:** parse_args(['--log-level', 'TRACE'])
- **Expected:** SystemExit
- **Links to:** REQ-05

**Test C-3: test_no_args_produces_backward_compat_config**
- **Purpose:** All no-args defaults match pre-refactor behavior
- **Expected:** season=2025, output_path='data/season_schedule.csv', level='INFO'
- **Links to:** REQ-06

---

## Edge Case Catalog

| Edge Case | Category | Expected | Test |
|-----------|----------|----------|------|
| --debug flag used | Input validation | SystemExit (not recognized) | E-1 (via Test 1.8) |
| Output path with spaces | Input boundary | Accepted as-is | E-2 |
| Very old season year | Input boundary | Accepted | E-3 |
| Future season year | Input boundary | Accepted | E-4 |
| Lowercase --log-level | Case sensitivity | SystemExit (no str.upper on F02) | E-5 |
| E2E + custom season | Combination | Both applied | E-6 |
| --debug not in help | Design verification | Not present | E-7 |

---

## Configuration Test Matrix

| Config Value | Default | Custom | Invalid |
|--------------|---------|--------|---------|
| season | C-1 | I-6 | Test 1.4 |
| log_level | Test 5.1 | Test 5.2 | C-2 |
| e2e_test | Test 1.6 | Test 1.7 | - |

---

## Validation Loop Summary

**Rounds Executed:** 3  
**Issues Found:** 0 per round
**Exit:** 3 consecutive clean rounds ✅

**Round 1:** All 7 requirements have test coverage ✅; no vague descriptions ✅
**Round 2:** Added E-5 (case sensitivity check for --log-level, F02 does NOT have str.upper unlike F06); added E-6
**Round 3:** Spot-checked REQ-04 (E2E max_weeks=1 covered), REQ-02 (NFL_SEASON removed covered), REQ-06 (backward compat covered) ✅ PASSED

---

## Next Steps

This file will be merged into `implementation_plan.md` during S5.P1.I1.
