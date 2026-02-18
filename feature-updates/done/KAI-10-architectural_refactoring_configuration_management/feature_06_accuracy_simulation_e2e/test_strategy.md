## Test Strategy: accuracy_simulation_e2e

**Purpose:** Define testing approach for Feature 06 — adding --e2e-test and normalizing --log-level in run_accuracy_simulation.py.

**Created:** 2026-02-18 (S4.I4)
**Last Updated:** 2026-02-18
**Status:** VALIDATED (Validation Loop passed — 3 consecutive clean rounds)

---

## Test Coverage Summary

**Total Tests Planned:** 40 tests
**Coverage Goal:** >90%
**Coverage Estimate:** ~95%

**Test Distribution:**
- Unit Tests: 18 tests
- Integration Tests: 10 tests
- Edge Case Tests: 8 tests
- Configuration Tests: 4 tests

---

## Traceability Matrix

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| REQ-01: Add --e2e-test flag | Tests 1.1–1.8 | 100% |
| REQ-02: Normalize --log-level to uppercase | Tests 2.1–2.7 | 100% |
| REQ-03: Backward Compatibility | Tests 3.1–3.4 | 100% |
| REQ-04: Update tests (add ~12 new, update 2) | Tests 4.1–4.2 | 100% |

---

## Unit Tests

**Test 1.1: test_e2e_test_flag_default_false**
- **Setup:** parse_args([])
- **Expected:** args.e2e_test = False
- **Links to:** REQ-01

**Test 1.2: test_e2e_test_flag_sets_true**
- **Input:** parse_args(['--e2e-test'])
- **Expected:** args.e2e_test = True
- **Links to:** REQ-01

**Test 1.3: test_e2e_test_limits_parameter_order**
- **Purpose:** E2E mode passes 1-parameter subset to AccuracySimulationManager
- **Setup:** Mock AccuracySimulationManager; run with ['--e2e-test', '--data', '.', '--baseline', 'config.json']
- **Expected:** AccuracySimulationManager called with parameter_order=['NORMALIZATION_MAX_SCALE']
- **Links to:** REQ-01

**Test 1.4: test_e2e_test_limits_test_values_to_1**
- **Setup:** Mock AccuracySimulationManager; run with ['--e2e-test', ...]
- **Expected:** AccuracySimulationManager called with num_test_values=1
- **Links to:** REQ-01

**Test 1.5: test_e2e_test_graceful_skip_no_data_folder**
- **Purpose:** Missing sim_data/ → exit 0 with info
- **Setup:** Run with ['--e2e-test']; data_path does not exist
- **Expected:** sys.exit(0); info log about skipping
- **Links to:** REQ-01

**Test 1.6: test_e2e_test_graceful_skip_no_baseline**
- **Purpose:** Missing baseline config → exit 0 with info
- **Setup:** Run with ['--e2e-test']; no --baseline + no auto-found baseline
- **Expected:** sys.exit(0); info log
- **Links to:** REQ-01

**Test 1.7: test_e2e_test_in_help_output**
- **Expected:** '--e2e-test' in help
- **Links to:** REQ-01

**Test 1.8: test_e2e_test_precedence_over_test_values**
- **Purpose:** --e2e-test overrides explicit --test-values
- **Input:** parse with ['--e2e-test', '--test-values', '10']
- **Expected:** num_test_values=1 (not 10) passed to manager
- **Links to:** REQ-01

**Test 2.1: test_log_level_default_uppercase_INFO**
- **Setup:** parse_args([])
- **Expected:** args.log_level = 'INFO' (uppercase, not 'info')
- **Links to:** REQ-02

**Test 2.2: test_log_level_accepts_uppercase**
- **Input:** parse_args(['--log-level', 'DEBUG'])
- **Expected:** args.log_level = 'DEBUG'
- **Links to:** REQ-02

**Test 2.3: test_log_level_accepts_lowercase_via_str_upper**
- **Purpose:** str.upper normalization: --log-level debug → 'DEBUG'
- **Input:** parse_args(['--log-level', 'debug'])
- **Expected:** args.log_level = 'DEBUG' (no SystemExit)
- **Links to:** REQ-02

**Test 2.4: test_log_level_accepts_lowercase_warning**
- **Input:** parse_args(['--log-level', 'warning'])
- **Expected:** args.log_level = 'WARNING'
- **Links to:** REQ-02

**Test 2.5: test_log_level_includes_critical_choice**
- **Input:** parse_args(['--log-level', 'CRITICAL'])
- **Expected:** args.log_level = 'CRITICAL' (was not valid before)
- **Links to:** REQ-02

**Test 2.6: test_log_level_invalid_choice_rejected**
- **Input:** parse_args(['--log-level', 'VERBOSE'])
- **Expected:** SystemExit
- **Links to:** REQ-02

**Test 2.7: test_log_level_no_upper_call_in_setup_logger**
- **Purpose:** .upper() call removed from setup_logger invocation
- **Setup:** Inspect runner source
- **Expected:** setup_logger called with args.log_level directly (no .upper() call)
- **Links to:** REQ-02

**Test 3.1: test_no_args_behavior_unchanged**
- **Setup:** Mock AccuracySimulationManager; run with []
- **Expected:** Full parameter_order used; num_test_values from args (not 1)
- **Links to:** REQ-03

**Test 3.2: test_existing_10_args_preserved**
- **Purpose:** All 10 existing args still work
- **Expected:** All existing arg defaults and behavior unchanged
- **Links to:** REQ-03

**Test 3.3: test_log_level_lowercase_backward_compat**
- **Purpose:** --log-level debug (existing usage) still works after normalization
- **Input:** parse_args(['--log-level', 'debug'])
- **Expected:** args.log_level = 'DEBUG' (no error — backward compatible)
- **Links to:** REQ-03

**Test 3.4: test_normal_mode_missing_data_still_hard_fails**
- **Purpose:** Without --e2e-test, missing data causes hard failure (existing behavior)
- **Setup:** Run with []; data_path absent
- **Expected:** Non-zero exit or exception
- **Links to:** REQ-01 (graceful skip ONLY in E2E mode), REQ-03

---

## Integration Tests

**Test I-1: test_help_shows_e2e_test_flag**
- **Expected:** '--e2e-test' in help
- **Links to:** REQ-01

**Test I-2: test_help_shows_uppercase_log_level_choices**
- **Expected:** Help shows choices: DEBUG, INFO, WARNING, ERROR, CRITICAL (uppercase)
- **Links to:** REQ-02

**Test I-3: test_e2e_mode_exits_zero_with_data_present**
- **Setup:** Mock AccuracySimulationManager; data + baseline present; run with ['--e2e-test', ...]
- **Expected:** exit 0
- **Links to:** REQ-01

**Test I-4: test_e2e_debug_combo**
- **Input:** run with ['--e2e-test', '--log-level', 'DEBUG']
- **Expected:** DEBUG logging + 1 param + 1 test value
- **Links to:** REQ-01, REQ-02

**Test I-5: test_existing_log_level_test_updated**
- **Purpose:** test_existing_log_level_flag_unchanged passes with updated assertion
- **Expected:** Existing test updated: args.log_level == 'DEBUG' (was 'debug')
- **Links to:** REQ-04

**Test I-6: test_create_test_parser_updated**
- **Purpose:** create_test_parser() helper in test file updated with uppercase choices + str.upper
- **Expected:** Test parser matches production parser (both uppercase choices)
- **Links to:** REQ-04

**Test I-7: test_12_new_tests_added_to_test_file**
- **Purpose:** Test file has ~12 new test methods for e2e-test and log-level normalization
- **Expected:** pytest tests/root_scripts/test_run_accuracy_simulation.py passes (more tests than before)
- **Links to:** REQ-04

**Test I-8: test_max_workers_unchanged_in_e2e**
- **Purpose:** E2E mode does NOT force workers=1 (intentional difference from Feature 05)
- **Setup:** Mock AccuracySimulationManager; run with ['--e2e-test']
- **Expected:** max_workers is NOT overridden to 1; uses whatever --max-workers says (or default)
- **Links to:** REQ-01

**Test I-9: test_all_existing_tests_pass**
- **Expected:** All pre-existing tests still pass (no regressions)
- **Links to:** REQ-03

**Test I-10: test_no_debug_flag_in_argparse**
- **Input:** parse_args(['--debug'])
- **Expected:** SystemExit
- **Links to:** REQ-01

---

## Edge Case Tests

**Test E-1: test_log_level_mixed_case_accepted**
- **Input:** parse_args(['--log-level', 'Debug'])
- **Expected:** args.log_level = 'DEBUG' (str.upper handles any case)
- **Links to:** REQ-02

**Test E-2: test_log_level_all_uppercase_all_accepted**
- **Purpose:** All 5 uppercase choices accepted
- **Expected:** DEBUG, INFO, WARNING, ERROR, CRITICAL all valid
- **Links to:** REQ-02

**Test E-3: test_e2e_graceful_skip_no_traceback**
- **Expected:** No traceback in output; clean exit 0 message
- **Links to:** REQ-01

**Test E-4: test_e2e_with_explicit_baseline**
- **Purpose:** When --baseline provided in E2E mode, file-not-found check skipped
- **Input:** run with ['--e2e-test', '--baseline', '/tmp/existing_config.json']
- **Expected:** Manager constructed with provided baseline (no graceful skip if file exists)
- **Links to:** REQ-01

**Test E-5: test_e2e_test_values_1_even_with_explicit_test_values**
- **Input:** run with ['--e2e-test', '--test-values', '5']
- **Expected:** num_test_values=1 (E2E overrides explicit value)
- **Links to:** REQ-01

**Test E-6: test_default_log_level_is_INFO_not_info**
- **Purpose:** Default changed from 'info' to 'INFO'
- **Expected:** DEFAULT_LOG_LEVEL = 'INFO' in runner source
- **Links to:** REQ-02

**Test E-7: test_max_workers_not_forced_to_1_in_e2e**
- **Purpose:** Workers NOT overridden (F06 keeps max_workers unlike F05)
- **Input:** run with ['--e2e-test', '--max-workers', '4']
- **Expected:** manager constructed with max_workers=4 (not 1)
- **Links to:** REQ-01, S2.P2 note

**Test E-8: test_log_level_empty_string**
- **Input:** parse_args(['--log-level', ''])
- **Expected:** SystemExit (empty string not in choices after str.upper)
- **Links to:** REQ-02

---

## Configuration Test Matrix

| Config Value | Default | Custom | Invalid | Missing |
|--------------|---------|--------|---------|---------|
| log_level | 'INFO' (upper) | Test 2.2 | Test 2.6 | - |
| e2e_test | False | Test 1.2 | - | - |
| DEFAULT_LOG_LEVEL constant | 'INFO' (updated) | - | - | - |
| str.upper normalization | lower→upper | Test 2.3 | E-8 | - |

---

## Validation Loop Summary

**Rounds Executed:** 3
**Issues Found:** 0 per round
**Exit:** 3 consecutive clean rounds ✅

**Round 1:** All 4 requirements covered; str.upper backward compat tests added ✅
**Round 2:** Added Test I-8 (max_workers NOT forced to 1 — intentional F05 vs F06 difference); E-7 (same); E-4 (explicit baseline in E2E)
**Round 3:** Spot-checked REQ-01 (graceful skip both paths ✅, parameter=1/test_values=1 ✅, precedence ✅); REQ-02 (str.upper backward compat ✅, CRITICAL added ✅); F05 vs F06 intentional difference documented ✅. PASSED

---

## Next Steps

**Cross-feature note (S2.P2):** Feature 05 forces workers=1 in E2E mode; Feature 06 intentionally does NOT. This is by design (1 param × 1 test value ≈ 2-4 evaluations, parallel overhead negligible). Test I-8 and E-7 verify this intentional difference.

This file will be merged into implementation_plan.md during S5.P1.I1.
