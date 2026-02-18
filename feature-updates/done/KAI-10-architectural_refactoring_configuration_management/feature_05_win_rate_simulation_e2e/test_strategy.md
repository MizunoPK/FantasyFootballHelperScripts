## Test Strategy: win_rate_simulation_e2e

**Purpose:** Define testing approach for Feature 05 — adding --e2e-test and --log-level to run_win_rate_simulation.py.

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
| REQ-01: Add 2 universal CLI args | Tests 1.1–1.8 | 100% |
| REQ-02: Remove LOGGING_LEVEL constant | Tests 2.1–2.3 | 100% |
| REQ-03: E2E Test Mode (mode=single/sims=1/workers=1) | Tests 3.1–3.7 | 100% |
| REQ-04: --log-level behavior | Tests 4.1–4.3 | 100% |
| REQ-05: Backward Compatibility | Tests 5.1–5.4 | 100% |
| REQ-06: Update tests (add new tests, preserve 28) | Tests 6.1–6.2 | 100% |

---

## Unit Tests

**Test 1.1: test_argparse_e2e_test_flag_default_false**
- **Setup:** parse_args([])
- **Expected:** args.e2e_test = False
- **Links to:** REQ-01

**Test 1.2: test_argparse_e2e_test_flag_sets_true**
- **Input:** parse_args(['--e2e-test'])
- **Expected:** args.e2e_test = True
- **Links to:** REQ-01

**Test 1.3: test_argparse_log_level_default_info**
- **Setup:** parse_args([])
- **Expected:** args.log_level = 'INFO'
- **Links to:** REQ-01

**Test 1.4: test_argparse_log_level_choices_uppercase**
- **Purpose:** Only uppercase choices accepted; no str.upper normalization
- **Input:** parse_args(['--log-level', 'TRACE'])
- **Expected:** SystemExit
- **Links to:** REQ-01, REQ-04

**Test 1.5: test_argparse_log_level_valid_choices**
- **Purpose:** DEBUG/INFO/WARNING/ERROR/CRITICAL all accepted
- **Expected:** All 5 accepted without error
- **Links to:** REQ-01

**Test 1.6: test_argparse_no_debug_flag**
- **Input:** parse_args(['--debug'])
- **Expected:** SystemExit
- **Links to:** REQ-01

**Test 1.7: test_argparse_e2e_test_in_help**
- **Expected:** '--e2e-test' in help output
- **Links to:** REQ-01

**Test 1.8: test_argparse_log_level_in_help**
- **Expected:** '--log-level' in help output
- **Links to:** REQ-01

**Test 2.1: test_logging_level_constant_removed**
- **Purpose:** LOGGING_LEVEL = 'INFO' no longer at module level
- **Setup:** Inspect run_win_rate_simulation module
- **Expected:** No LOGGING_LEVEL module-level attribute
- **Links to:** REQ-02

**Test 2.2: test_log_name_constant_preserved**
- **Purpose:** LOG_NAME = 'win_rate_simulation' still present (required by tests)
- **Expected:** LOG_NAME present at module level
- **Links to:** REQ-02

**Test 2.3: test_setup_logger_uses_args_log_level**
- **Purpose:** setup_logger called with args.log_level, not LOGGING_LEVEL constant
- **Setup:** Mock setup_logger; parse with ['--log-level', 'WARNING']
- **Expected:** setup_logger called with 'WARNING' (not hardcoded 'INFO')
- **Links to:** REQ-02, REQ-04

**Test 3.1: test_e2e_mode_forces_single_mode**
- **Setup:** Mock SimulationManager; parse with ['--e2e-test']
- **Expected:** args.mode overridden to 'single' before manager creation
- **Links to:** REQ-03

**Test 3.2: test_e2e_mode_forces_sims_1**
- **Setup:** Mock SimulationManager; parse with ['--e2e-test']
- **Expected:** args.sims overridden to 1
- **Links to:** REQ-03

**Test 3.3: test_e2e_mode_forces_workers_1**
- **Setup:** Mock SimulationManager; parse with ['--e2e-test']
- **Expected:** args.workers overridden to 1
- **Links to:** REQ-03

**Test 3.4: test_e2e_mode_graceful_skip_no_baseline**
- **Purpose:** Missing baseline config → exit 0 with info message
- **Setup:** Run with ['--e2e-test']; baseline folder absent
- **Expected:** sys.exit(0) called; info log about skipping
- **Links to:** REQ-03

**Test 3.5: test_e2e_mode_graceful_skip_no_sim_data**
- **Purpose:** Missing sim_data folder → exit 0 with info message
- **Setup:** Run with ['--e2e-test']; sim_data folder absent
- **Expected:** sys.exit(0) called; info log about skipping
- **Links to:** REQ-03

**Test 3.6: test_e2e_precedence_over_sims_arg**
- **Purpose:** --e2e-test overrides explicit --sims
- **Setup:** parse with ['--e2e-test', '--sims', '10']
- **Expected:** sims forced to 1 (not 10)
- **Links to:** REQ-03

**Test 3.7: test_e2e_precedence_over_workers_arg**
- **Setup:** parse with ['--e2e-test', '--workers', '8']
- **Expected:** workers forced to 1 (not 8)
- **Links to:** REQ-03

**Test 4.1: test_log_level_debug_accepted**
- **Input:** parse_args(['--log-level', 'DEBUG'])
- **Expected:** args.log_level = 'DEBUG'
- **Links to:** REQ-04

**Test 4.2: test_log_level_critical_accepted**
- **Input:** parse_args(['--log-level', 'CRITICAL'])
- **Expected:** args.log_level = 'CRITICAL'
- **Links to:** REQ-04

**Test 4.3: test_log_level_lowercase_rejected**
- **Purpose:** Lowercase not accepted (no str.upper on F05)
- **Input:** parse_args(['--log-level', 'debug'])
- **Expected:** SystemExit (choice validation fails without str.upper)
- **Links to:** REQ-04

---

## Integration Tests

**Test I-1: test_help_shows_e2e_test_and_log_level**
- **Expected:** Both new args in help
- **Links to:** REQ-01

**Test I-2: test_no_args_behavior_unchanged**
- **Purpose:** Default behavior: iterative mode, INFO logging
- **Setup:** Mock SimulationManager; run with []
- **Expected:** mode='iterative' (default), level='INFO'
- **Links to:** REQ-05

**Test I-3: test_existing_single_mode_preserved**
- **Input:** run with ['single', '--sims', '5']
- **Expected:** SimulationManager called with mode='single', sims=5
- **Links to:** REQ-05

**Test I-4: test_enable_log_file_preserved**
- **Input:** run with ['--enable-log-file']
- **Expected:** setup_logger called with log_to_file=True
- **Links to:** REQ-05

**Test I-5: test_e2e_mode_exits_zero_with_data_present**
- **Setup:** Mock SimulationManager; provide sim_data and baseline; run with ['--e2e-test']
- **Expected:** exit code 0
- **Links to:** REQ-03

**Test I-6: test_e2e_debug_combo**
- **Input:** run with ['--e2e-test', '--log-level', 'DEBUG']
- **Expected:** level='DEBUG' + mode='single'/sims=1/workers=1
- **Links to:** REQ-03, REQ-04

**Test I-7: test_existing_28_tests_still_pass**
- **Purpose:** All 28 pre-existing tests pass after changes
- **Expected:** pytest tests/root_scripts/test_run_win_rate_simulation.py → 28+ passed
- **Links to:** REQ-06

**Test I-8: test_log_level_replaces_logging_level_constant_in_setup_logger**
- **Expected:** setup_logger(LOG_NAME, args.log_level, ...) — no LOGGING_LEVEL constant reference
- **Links to:** REQ-02

**Test I-9: test_graceful_skip_non_e2e_mode_still_fails**
- **Purpose:** In normal mode, missing data still causes hard failure (existing behavior)
- **Setup:** Run with [] (no --e2e-test); sim_data absent
- **Expected:** Non-zero exit or exception (existing hard-fail behavior preserved)
- **Links to:** REQ-03 (graceful skip ONLY in E2E mode)

**Test I-10: test_no_logging_level_constant_in_setup_logger_call**
- **Purpose:** grep 'LOGGING_LEVEL' in runner source returns empty
- **Expected:** Empty result
- **Links to:** REQ-02

---

## Edge Case Tests

**Test E-1: test_e2e_mode_with_explicit_iterative_mode**
- **Input:** parse with ['--e2e-test'] (mode defaults to iterative)
- **Expected:** --e2e-test overrides to 'single' even when default mode is iterative
- **Links to:** REQ-03

**Test E-2: test_e2e_graceful_skip_no_traceback**
- **Purpose:** Graceful skip exits cleanly with no exception traceback
- **Expected:** sys.exit(0); no traceback in output
- **Links to:** REQ-03

**Test E-3: test_log_level_lowercase_rejected**
- Already covered by Test 4.3
- **Links to:** REQ-04

**Test E-4: test_e2e_with_enable_log_file**
- **Input:** run with ['--e2e-test', '--enable-log-file']
- **Expected:** Both applied — E2E overrides + log file enabled
- **Links to:** REQ-03, REQ-05

**Test E-5: test_no_debug_flag_in_help**
- **Expected:** '--debug' NOT in help
- **Links to:** REQ-01

**Test E-6: test_e2e_does_not_change_log_level**
- **Purpose:** --e2e-test alone does not change log level (stays INFO)
- **Input:** parse with ['--e2e-test'] (no --log-level)
- **Expected:** log_level='INFO'
- **Links to:** REQ-03, REQ-04

**Test E-7: test_existing_sims_arg_still_works_without_e2e**
- **Input:** run with ['single', '--sims', '3']
- **Expected:** SimulationManager called with sims=3 (not overridden since no --e2e-test)
- **Links to:** REQ-05

---

## Configuration Test Matrix

| Config Value | Default | Custom | Invalid |
|--------------|---------|--------|---------|
| log_level | INFO | Test 4.1 (DEBUG) | Test 1.4 |
| e2e_test | False | Test 1.2 | - |
| LOGGING_LEVEL constant | Removed | N/A | N/A |

---

## Validation Loop Summary

**Rounds Executed:** 3
**Issues Found:** 0 per round
**Exit:** 3 consecutive clean rounds ✅

**Round 1:** All 6 requirements covered ✅; graceful skip scenarios covered (both baseline and sim_data) ✅
**Round 2:** Added Test I-9 (non-E2E hard-fail preserved); E-6 (e2e doesn't change log level); E-2 (no traceback)
**Round 3:** Spot-checked REQ-03 (graceful skip both paths ✅, precedence over sims/workers/mode ✅); REQ-02 (LOGGING_LEVEL removed ✅); 28 existing tests preserved ✅. PASSED

---

## Next Steps

This file will be merged into implementation_plan.md during S5.P1.I1.
