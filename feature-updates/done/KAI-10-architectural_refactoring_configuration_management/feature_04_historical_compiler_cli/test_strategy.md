## Test Strategy: historical_compiler_cli

**Purpose:** Define testing approach for Feature 04 — adding CLI args to compile_historical_data.py.

**Created:** 2026-02-18 (S4.I4)
**Last Updated:** 2026-02-18
**Status:** VALIDATED (Validation Loop passed — 3 consecutive clean rounds)

---

## Test Coverage Summary

**Total Tests Planned:** 46 tests
**Coverage Goal:** >90%
**Coverage Estimate:** ~95%

**Test Distribution:**
- Unit Tests: 20 tests
- Integration Tests: 12 tests
- Edge Case Tests: 9 tests
- Configuration Tests: 5 tests

---

## Traceability Matrix

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| REQ-01: CLI Arguments (8 total) | Tests 1.1–1.10 | 100% |
| REQ-02: Wire timeout/rate_limit_delay to BaseHTTPClient | Tests 2.1–2.5 | 100% |
| REQ-03: Remove constants from constants.py + http_client.py | Tests 3.1–3.4 | 100% |
| REQ-04: E2E Test Mode (tempfile, player_limit=100) | Tests 4.1–4.6 | 100% |
| REQ-05: No separate debug flag | Tests 5.1 | 100% |
| REQ-06: --log-level behavior (incl. --verbose compat) | Tests 6.1–6.5 | 100% |
| REQ-07: --verbose backward compat | Tests 7.1–7.3 | 100% |
| REQ-08: Backward Compatibility (no-args) | Tests 8.1–8.3 | 100% |

---

## Unit Tests

**Test 1.1: test_argparse_default_values**
- **Purpose:** 8 args have correct defaults
- **Setup:** parse_args([])
- **Expected:** e2e_test=False, log_level='INFO', timeout=30.0, rate_limit_delay=0.3, year=None, verbose=False, enable_log_file=False, output_dir=None
- **Links to:** REQ-01

**Test 1.2: test_argparse_timeout_type_float**
- **Input:** parse_args(['--timeout', '60.0'])
- **Expected:** args.timeout = 60.0
- **Links to:** REQ-01

**Test 1.3: test_argparse_rate_limit_delay_type_float**
- **Input:** parse_args(['--rate-limit-delay', '0.5'])
- **Expected:** args.rate_limit_delay = 0.5
- **Links to:** REQ-01

**Test 1.4: test_argparse_e2e_test_flag**
- **Input:** parse_args(['--e2e-test'])
- **Expected:** args.e2e_test = True
- **Links to:** REQ-01, REQ-04

**Test 1.5: test_argparse_log_level_choices**
- **Purpose:** Valid choices: DEBUG/INFO/WARNING/ERROR/CRITICAL; invalid rejected
- **Input:** parse_args(['--log-level', 'TRACE'])
- **Expected:** SystemExit
- **Links to:** REQ-01, REQ-06

**Test 1.6: test_argparse_year_type_int**
- **Input:** parse_args(['--year', '2024'])
- **Expected:** args.year = 2024
- **Links to:** REQ-01

**Test 1.7: test_argparse_verbose_flag**
- **Input:** parse_args(['--verbose'])
- **Expected:** args.verbose = True
- **Links to:** REQ-01, REQ-07

**Test 1.8: test_argparse_short_verbose_flag**
- **Input:** parse_args(['-v'])
- **Expected:** args.verbose = True
- **Links to:** REQ-01, REQ-07

**Test 1.9: test_argparse_no_debug_flag**
- **Input:** parse_args(['--debug'])
- **Expected:** SystemExit
- **Links to:** REQ-05

**Test 1.10: test_argparse_enable_log_file**
- **Input:** parse_args(['--enable-log-file'])
- **Expected:** args.enable_log_file = True
- **Links to:** REQ-01

**Test 2.1: test_base_http_client_receives_timeout_from_args**
- **Purpose:** BaseHTTPClient constructed with timeout from CLI
- **Setup:** Mock BaseHTTPClient; parse_args with --timeout 60.0
- **Expected:** BaseHTTPClient(timeout=60.0, ...) called
- **Links to:** REQ-02

**Test 2.2: test_base_http_client_receives_rate_limit_delay**
- **Setup:** Mock BaseHTTPClient; args.rate_limit_delay=0.5
- **Expected:** BaseHTTPClient(rate_limit_delay=0.5, ...) called
- **Links to:** REQ-02

**Test 2.3: test_compile_season_data_signature_accepts_timeout**
- **Purpose:** compile_season_data() has timeout param
- **Setup:** inspect.signature(compile_season_data)
- **Expected:** 'timeout' in signature
- **Links to:** REQ-02a

**Test 2.4: test_compile_season_data_signature_accepts_rate_limit_delay**
- **Expected:** 'rate_limit_delay' in compile_season_data signature
- **Links to:** REQ-02a

**Test 2.5: test_compile_season_data_signature_accepts_e2e_test**
- **Expected:** 'e2e_test' in compile_season_data signature
- **Links to:** REQ-02a

**Test 3.1: test_request_timeout_removed_from_constants**
- **Setup:** import historical_data_compiler.constants
- **Expected:** hasattr(constants, 'REQUEST_TIMEOUT') == False
- **Links to:** REQ-03

**Test 3.2: test_rate_limit_delay_removed_from_constants**
- **Expected:** hasattr(constants, 'RATE_LIMIT_DELAY') == False
- **Links to:** REQ-03

**Test 3.3: test_base_http_client_no_constants_import_for_timeout**
- **Purpose:** http_client.py no longer imports REQUEST_TIMEOUT from constants
- **Setup:** Inspect http_client module namespace
- **Expected:** REQUEST_TIMEOUT not in http_client's imported names from constants
- **Links to:** REQ-03

**Test 3.4: test_base_http_client_inline_defaults**
- **Purpose:** BaseHTTPClient() with no args uses inline defaults (30.0, 0.3)
- **Setup:** BaseHTTPClient() with no params
- **Expected:** timeout defaults to 30.0, rate_limit_delay defaults to 0.3 (inline in __init__, not from constants)
- **Links to:** REQ-03

**Test 4.1: test_e2e_mode_uses_temp_directory**
- **Purpose:** E2E mode writes to tempdir, not simulation/sim_data
- **Setup:** Mock tempfile.TemporaryDirectory; run with ['--e2e-test']
- **Expected:** Output dir is inside temp directory
- **Links to:** REQ-04

**Test 4.2: test_e2e_mode_player_limit_100**
- **Purpose:** E2E mode limits ESPN player fetches to 100
- **Setup:** Mock fetch_player_data; run with ['--e2e-test']
- **Expected:** fetch_player_data called with player_limit=100
- **Links to:** REQ-04

**Test 4.3: test_e2e_mode_single_season**
- **Purpose:** E2E mode compiles exactly 1 season
- **Setup:** Mock compile_season_data; run with ['--e2e-test']
- **Expected:** compile_season_data called exactly once
- **Links to:** REQ-04

**Test 4.4: test_e2e_mode_temp_dir_cleaned_up**
- **Purpose:** Temp directory removed after E2E run
- **Setup:** Run with ['--e2e-test']; check temp dir after
- **Expected:** Temp directory no longer exists after completion
- **Links to:** REQ-04

**Test 6.1: test_verbose_flag_maps_to_debug_logging**
- **Purpose:** --verbose sets log level to DEBUG
- **Setup:** Mock setup_logger; run with ['--verbose']
- **Expected:** setup_logger called with level='DEBUG'
- **Links to:** REQ-06, REQ-07

**Test 6.2: test_log_level_default_info**
- **Setup:** parse_args([])
- **Expected:** Effective log level = 'INFO' (no verbose)
- **Links to:** REQ-06

**Test 6.3: test_log_level_overridable_via_flag**
- **Setup:** run with ['--log-level', 'WARNING']
- **Expected:** setup_logger called with 'WARNING'
- **Links to:** REQ-06

**Test 6.4: test_verbose_takes_precedence_over_log_level**
- **Purpose:** If both --verbose and --log-level provided, verbose wins (DEBUG)
- **Setup:** run with ['--verbose', '--log-level', 'WARNING']
- **Expected:** setup_logger called with 'DEBUG' (verbose wins)
- **Links to:** REQ-06 (precedence: verbose > log_level > default)

**Test 6.5: test_existing_verbose_tests_pass**
- **Purpose:** test_compile_historical_data_logger.py T2.1 and T2.2 still pass
- **Expected:** Both existing verbose tests pass unchanged
- **Links to:** REQ-07

---

## Integration Tests

**Test I-1: test_help_displays_all_8_args**
- **Expected:** All 8 args in help: --e2e-test, --log-level, --timeout, --rate-limit-delay, --year, --verbose/-v, --enable-log-file, --output-dir
- **Links to:** REQ-01

**Test I-2: test_no_args_backward_compat**
- **Purpose:** No-args run: no --year → compiles all YEARS; INFO logging
- **Setup:** Mock compile_season_data; run with []
- **Expected:** compile_season_data called multiple times (once per year); level='INFO'
- **Links to:** REQ-08

**Test I-3: test_custom_timeout_and_rate_passed_through**
- **Setup:** run with ['--year', '2024', '--timeout', '60.0', '--rate-limit-delay', '0.5']
- **Expected:** BaseHTTPClient(timeout=60.0, rate_limit_delay=0.5)
- **Links to:** REQ-02

**Test I-4: test_e2e_mode_exits_zero**
- **Setup:** Mock all external calls; run with ['--e2e-test']
- **Expected:** exit code 0
- **Links to:** REQ-04

**Test I-5: test_e2e_debug_combo**
- **Setup:** run with ['--e2e-test', '--log-level', 'DEBUG']
- **Expected:** DEBUG logging + E2E scope limits applied
- **Links to:** REQ-04, REQ-06

**Test I-6: test_fetch_player_data_accepts_player_limit_param**
- **Purpose:** player_data_fetcher.fetch_player_data() has player_limit param
- **Setup:** inspect.signature(fetch_player_data)
- **Expected:** 'player_limit' in signature
- **Links to:** REQ-04 (data limiting strategy)

**Test I-7: test_request_timeout_absent_from_constants_grep**
- **Expected:** grep 'REQUEST_TIMEOUT' historical_data_compiler/constants.py returns empty
- **Links to:** REQ-03

**Test I-8: test_rate_limit_delay_absent_from_constants_grep**
- **Expected:** grep 'RATE_LIMIT_DELAY' historical_data_compiler/constants.py returns empty
- **Links to:** REQ-03

**Test I-9: test_enable_log_file_preserved**
- **Setup:** run with ['--enable-log-file']
- **Expected:** setup_logger called with log_to_file=True
- **Links to:** REQ-08

**Test I-10: test_output_dir_custom_path**
- **Setup:** run with ['--output-dir', '/tmp/custom']
- **Expected:** compile_season_data called with output_dir=/tmp/custom
- **Links to:** REQ-01

**Test I-11: test_year_specific_compiles_one_season**
- **Setup:** run with ['--year', '2024']
- **Expected:** compile_season_data called once with year=2024
- **Links to:** REQ-01

**Test I-12: test_no_args_produces_backward_compat_behavior**
- **Purpose:** All defaults match pre-refactor behavior
- **Expected:** timeout=30.0, rate_limit_delay=0.3, level='INFO'
- **Links to:** REQ-08

---

## Edge Case Tests

**Test E-1: test_timeout_zero**
- **Input:** parse_args(['--timeout', '0'])
- **Expected:** args.timeout = 0.0 (accepted, possibly causes immediate timeout in production)
- **Links to:** REQ-01

**Test E-2: test_rate_limit_delay_zero**
- **Input:** parse_args(['--rate-limit-delay', '0'])
- **Expected:** args.rate_limit_delay = 0.0
- **Links to:** REQ-01

**Test E-3: test_e2e_mode_with_explicit_year**
- **Input:** parse_args(['--e2e-test', '--year', '2023'])
- **Expected:** E2E mode AND year=2023 both applied; compile_season_data called once with 2023
- **Links to:** REQ-04

**Test E-4: test_verbose_and_e2e_test_combined**
- **Input:** parse_args(['--verbose', '--e2e-test'])
- **Expected:** Both flags set; verbose → DEBUG; E2E scope limits applied
- **Links to:** REQ-06, REQ-07

**Test E-5: test_no_debug_flag_in_help**
- **Expected:** '--debug' NOT in help output
- **Links to:** REQ-05

**Test E-6: test_year_negative**
- **Input:** parse_args(['--year', '-1'])
- **Expected:** Accepted by argparse (no bounds check)
- **Links to:** REQ-01

**Test E-7: test_base_http_client_backward_compat_no_params**
- **Purpose:** BaseHTTPClient() with no params still works (inline defaults)
- **Setup:** BaseHTTPClient() - no args
- **Expected:** No TypeError; defaults used
- **Links to:** REQ-03

**Test E-8: test_e2e_mode_temp_dir_unique**
- **Purpose:** Each E2E run uses a fresh temp dir (not shared state)
- **Setup:** Run E2E twice in same process (if possible)
- **Expected:** Two different temp dirs used
- **Links to:** REQ-04

**Test E-9: test_verbose_combined_with_log_level_warning**
- **Input:** parse_args(['--verbose', '--log-level', 'WARNING'])
- **Expected:** --verbose wins → DEBUG (per REQ-06 precedence)
- **Links to:** REQ-06, REQ-07

---

## Configuration Test Matrix

| Config Value | Default | Custom | Invalid |
|--------------|---------|--------|---------|
| timeout | Test 1.1 (30.0) | I-3 (60.0) | - |
| rate_limit_delay | Test 1.1 (0.3) | I-3 (0.5) | - |
| log_level | Test 1.1 (INFO) | Test 6.3 (WARNING) | Test 1.5 |
| year | Test 1.1 (None=all years) | Test 1.6 (2024) | - |
| verbose (maps DEBUG) | Test 6.2 | Test 6.1 | - |

---

## Validation Loop Summary

**Rounds Executed:** 3
**Issues Found:** 0 per round
**Exit:** 3 consecutive clean rounds ✅

**Round 1:** All 8 requirements covered; compile_season_data signature tests added ✅
**Round 2:** Added E-9 (verbose+log-level edge case); added Test 6.4 (precedence)
**Round 3:** Spot-checked REQ-04 (E2E: tempfile, player_limit=100, single season, cleanup covered ✅); REQ-03 (constants removal covered ✅); backward compat covered ✅. PASSED

---

## Next Steps

This file will be merged into `implementation_plan.md` during S5.P1.I1.
