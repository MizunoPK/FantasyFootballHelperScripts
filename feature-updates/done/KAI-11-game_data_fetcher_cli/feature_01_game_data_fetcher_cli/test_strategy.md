## Test Strategy: game_data_fetcher_cli

**Purpose:** Define testing approach for game_data_fetcher_cli feature

**Created:** 2026-02-19 (S4.I4)
**Last Updated:** 2026-02-19
**Status:** VALIDATED (Validation Loop passed with 3 consecutive clean rounds — Rounds 3, 4, 5)

---

## Test Coverage Summary

**Total Tests Planned:** 16 test scenarios
**Coverage Goal:** >90%
**Coverage Estimate:** 100% (all 11 requirements covered)

**Test Distribution:**
- Unit Tests: 3 (REQ-11 mandated: test_has_parse_args, test_parse_args_defaults, test_no_subprocess)
- Structural Tests: 2 (grep-based: verify REQ-03 + REQ-04 anti-pattern removal)
- CLI Smoke Tests: 7 (script execution: verify REQ-01 through REQ-10 + regression suite)
- Edge Case Tests: 4 (argparse validation: invalid choices, precedence rules)

**Note on scope:** This feature modifies 1 runner script + creates 1 test file. The test suite
is intentionally small and targeted. Comprehensive coverage is achieved through a combination of
unit tests (for argparse structure) and CLI smoke tests (for behavior verification).

---

## Test Coverage Matrix

| Requirement | Unit | Structural | Smoke | Edge Case | Total |
|-------------|------|------------|-------|-----------|-------|
| REQ-01: parse_args() + --e2e-test + --log-level | U1, U2 | — | C2 | E1 | 4 |
| REQ-02: Argparse defaults (season=2025, week=17) | U2 | — | C2 | E5 | 3 |
| REQ-03: Remove config import | — | S1 | C1 | — | 2 |
| REQ-04: Remove os.chdir() | U3 | S2 | C1 | E6 | 4 |
| REQ-05: Wire --log-level to setup_logger | — | — | C4 | — | 1 |
| REQ-06: E2E mode (/tmp, data/ unchanged, ≤180s) | — | — | C3 | E2 | 2 |
| REQ-07: --log-level choices + default 'INFO' | U2 | — | C2 | E1 | 3 |
| REQ-08: Backward compatibility (all defaults) | U2 | — | C6, C7 | — | 3 |
| REQ-09: --historical-season flag + precedence | U2 | — | C5 | E3 | 3 |
| REQ-10: --request-timeout default 30 + pass-through | U2 | — | C2, C3 | E4 | 3 |
| REQ-11: Test file with 3 tests + suite passes | U1, U2, U3 | — | C7 | — | 4 |

**Requirements with <90% coverage:** 0 ✅

---

## Traceability Matrix

| Test ID | Test Name | Requirements Covered |
|---------|-----------|---------------------|
| U1 | test_has_parse_args | REQ-01, REQ-11 |
| U2 | test_parse_args_defaults | REQ-01, REQ-02, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11 |
| U3 | test_no_subprocess | REQ-04, REQ-11 |
| S1 | Grep: "from config import" returns empty | REQ-03 |
| S2 | Grep: "os.chdir" returns empty | REQ-04 |
| C1 | Import test (no ImportError) | REQ-03, REQ-04 |
| C2 | Help output: 8 args, correct defaults | REQ-01, REQ-02, REQ-07, REQ-09, REQ-10 |
| C3 | E2E mode: /tmp only, data/ unchanged, ≤180s | REQ-06, REQ-08, REQ-10 |
| C4 | --log-level DEBUG: DEBUG lines visible | REQ-05, REQ-07 |
| C5 | --historical-season: "Historical season mode" in log | REQ-09 |
| C6 | No-args: defaults match pre-refactor | REQ-08 |
| C7 | Full pytest suite: 100% pass, 0 failures | REQ-08, REQ-11 |
| E1 | --log-level invalid/lowercase → SystemExit | REQ-01, REQ-07 |
| E2 | --e2e-test + --weeks: e2e takes precedence | REQ-06 |
| E3 | --historical-season + --current-week: historical wins | REQ-09 |
| E4 | --request-timeout non-int → SystemExit | REQ-10 |
| E5 | --season non-int → SystemExit | REQ-02 |
| E6 | Import succeeds from any CWD (sys.path absolute) | REQ-04 |

**Total test scenarios: 18** (16 above + E5, E6 added in edge case analysis)

---

## Unit Tests

Pattern reference: `TestRunPlayerFetcher` in `tests/root_scripts/test_root_scripts.py` lines 95–113.
New file: `tests/root_scripts/test_run_game_data_fetcher.py`

---

### Test U1: `test_has_parse_args`

**Purpose:** Verify `parse_args` function exists at module level and is callable
**Setup:** `import run_game_data_fetcher`
**Input:** N/A (introspection only)
**Expected:** `callable(run_game_data_fetcher.parse_args) is True`
**Links to:** REQ-01 (derived requirement: extract parse_args for testability), REQ-11

---

### Test U2: `test_parse_args_defaults`

**Purpose:** Verify `parse_args([])` produces all 6 correct defaults (single source of truth)
**Setup:** `import run_game_data_fetcher`
**Input:** `parse_args([])`
**Expected:**
- `args.season == 2025` (REQ-02: was None → config, now 2025 in argparse)
- `args.current_week == 17` (REQ-02: was None → config, now 17 in argparse)
- `args.log_level == 'INFO'` (REQ-07: default INFO)
- `args.e2e_test is False` (REQ-01: default False)
- `args.request_timeout == 30` (REQ-10: default 30)
- `args.historical_season is False` (REQ-09: default False)
**Links to:** REQ-01, REQ-02, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11

---

### Test U3: `test_no_subprocess`

**Purpose:** Verify runner does not import subprocess (anti-pattern check)
**Setup:** Inspect run_game_data_fetcher source or check module attributes
**Input:** N/A
**Expected:** `subprocess` not imported by run_game_data_fetcher
**Links to:** REQ-04 (broader anti-pattern removal verification), REQ-11

---

## Structural Tests

### Test S1: Grep — Config Import Removed

**Purpose:** Verify "from config import" fully removed from source
**Command:**
```bash
grep "from config import" run_game_data_fetcher.py
```
**Expected:** Empty output (exit code 1 — no matches)
**Failure:** Any output → config import not removed (REQ-03 not implemented)
**Links to:** REQ-03

---

### Test S2: Grep — os.chdir Removed

**Purpose:** Verify "os.chdir" fully removed from source
**Command:**
```bash
grep "os.chdir" run_game_data_fetcher.py
```
**Expected:** Empty output (exit code 1 — no matches)
**Failure:** Any output → os.chdir not removed (REQ-04 not implemented)
**Links to:** REQ-04

---

## CLI Smoke Tests

### Test C1: Import Test

**Purpose:** Verify runner imports without error after removing config dependency
**Command:**
```bash
python -c "import run_game_data_fetcher; print('OK')"
```
**Expected:** `OK` printed, exit code 0
**Failure:** ImportError for config module → REQ-03 not implemented; any other ImportError → sys.path broken (REQ-04)
**Links to:** REQ-03, REQ-04

---

### Test C2: Help Output — 8 Args with Correct Defaults

**Purpose:** Verify all 8 CLI args present with correct defaults
**Command:**
```bash
python run_game_data_fetcher.py --help
```
**Expected:**
- `--season` visible, default `2025`
- `--current-week` visible, default `17`
- `--output` visible
- `--weeks` visible
- `--e2e-test` visible (flag)
- `--log-level` visible, choices `{DEBUG,INFO,WARNING,ERROR,CRITICAL}`, default `INFO`
- `--request-timeout` visible, default `30`
- `--historical-season` visible (flag)
**Links to:** REQ-01, REQ-02, REQ-07, REQ-09, REQ-10

---

### Test C3: E2E Test Mode

**Purpose:** Verify E2E mode completes fast, writes to /tmp only, leaves data/ unchanged
**Commands:**
```bash
md5sum data/game_data.csv > /tmp/game_data_before.md5
time python run_game_data_fetcher.py --e2e-test
ls -la /tmp/game_data_e2e_test.csv
md5sum -c /tmp/game_data_before.md5
```
**Expected:**
- Exit code 0
- Completes in ≤180 seconds
- `/tmp/game_data_e2e_test.csv` exists and is non-empty
- `data/game_data.csv` checksum unchanged
- Log contains "E2E test mode: limiting to week 1"
**Links to:** REQ-06, REQ-08, REQ-10

---

### Test C4: Log-Level Passthrough

**Purpose:** Verify `--log-level` is wired to `setup_logger()` (not hardcoded "INFO")
**Command:**
```bash
python run_game_data_fetcher.py --e2e-test --log-level DEBUG 2>&1 | head -20
```
**Expected:** DEBUG-level log lines visible (lines containing "DEBUG")
**Failure:** No DEBUG lines → log_level not passed to setup_logger (REQ-05 not implemented)
**Links to:** REQ-05, REQ-07

---

### Test C5: Historical Season Flag

**Purpose:** Verify `--historical-season` sets current_week=18 with explicit log message
**Command:**
```bash
python run_game_data_fetcher.py --season 2024 --historical-season --e2e-test 2>&1 | grep -i "historical"
```
**Expected:**
- Exit code 0
- Log contains "Historical season mode" (REQ-09 exact message: "fetching all 18 weeks for {season}")
**Links to:** REQ-09

---

### Test C6: Backward Compatibility — No-Args Behavior

**Purpose:** Verify no-args defaults are identical to pre-refactor
**Command:**
```bash
python run_game_data_fetcher.py --help | grep -E "default|Default"
```
**Expected:**
- `--season` default: `2025`
- `--current-week` default: `17`
- `--log-level` default: `INFO`
- `--request-timeout` default: `30`
**Links to:** REQ-08

---

### Test C7: Full Regression Suite

**Purpose:** Verify 100% pass rate — all 3 new tests pass AND all existing tests still pass
**Command:**
```bash
pytest tests/ -v 2>&1 | tail -10
```
**Expected:**
- `tests/root_scripts/test_run_game_data_fetcher.py` listed with 3 tests
- All 3 new tests pass: `test_has_parse_args`, `test_parse_args_defaults`, `test_no_subprocess`
- 0 failures, 0 errors across entire test suite
**Links to:** REQ-08 (backward compat), REQ-11

---

## Edge Case Tests

### Test E1: --log-level Invalid/Lowercase → SystemExit

**Purpose:** Verify argparse rejects invalid and lowercase log-level values
**Inputs:**
- `parse_args(['--log-level', 'VERBOSE'])` → SystemExit code 2
- `parse_args(['--log-level', 'debug'])` → SystemExit code 2 (choices are uppercase)
**Expected:** SystemExit raised (argparse rejects non-matching choices)
**Links to:** REQ-01, REQ-07

---

### Test E2: --e2e-test + --weeks Conflict → E2E Wins

**Purpose:** Verify `--e2e-test` overrides `--weeks` (e2e takes precedence per REQ-06)
**Input:** `python run_game_data_fetcher.py --e2e-test --weeks 5,6,7`
**Expected:** E2E mode active: weeks=[1] (NOT weeks=[5,6,7])
**Log verification:** "E2E test mode: limiting to week 1" present in output
**Links to:** REQ-06

---

### Test E3: --historical-season + --current-week Conflict → Historical Wins

**Purpose:** Verify `--historical-season` overrides `--current-week` (per REQ-09)
**Input:** `python run_game_data_fetcher.py --historical-season --current-week 10 --e2e-test 2>&1 | grep -i "historical"`
**Expected:** "Historical season mode" logged (current_week=18, NOT 10)
**Links to:** REQ-09

---

### Test E4: --request-timeout Non-Integer → SystemExit

**Purpose:** Verify argparse rejects non-integer timeout
**Input:** `python run_game_data_fetcher.py --request-timeout abc`
**Expected:** SystemExit code 2 (argparse type=int rejects)
**Links to:** REQ-10

---

### Test E5: --season Non-Integer → SystemExit

**Purpose:** Verify argparse rejects non-integer season
**Input:** `python run_game_data_fetcher.py --season abc`
**Expected:** SystemExit code 2 (argparse type=int rejects)
**Links to:** REQ-02

---

### Test E6: Import Succeeds from Any CWD (sys.path Absolute)

**Purpose:** Verify sys.path uses `Path(__file__).parent` — absolute, not CWD-relative
**Context:** os.chdir() was removed; sys.path inserts moved to module level using Path(__file__).parent
**Expected:** `python -c "import run_game_data_fetcher; print('OK')"` succeeds regardless of CWD
**Links to:** REQ-04

---

## Edge Case Catalog

| Edge Case | Category | Expected Behavior | Test |
|-----------|----------|-------------------|------|
| --log-level lowercase (debug) | Argparse validation | SystemExit code 2 | E1 |
| --log-level invalid (VERBOSE) | Argparse validation | SystemExit code 2 | E1 |
| --e2e-test + --weeks conflict | Precedence | e2e wins: weeks=[1] | E2 |
| --historical-season + --current-week | Precedence | historical wins: current_week=18 | E3 |
| --request-timeout non-int (abc) | Argparse validation | SystemExit code 2 | E4 |
| --season non-int (abc) | Argparse validation | SystemExit code 2 | E5 |
| Import from any CWD (no os.chdir) | Path handling | Import succeeds | E6 |

**Total edge cases: 7. All have tests. ✅**

---

## Configuration Tests

**Context:** This feature REMOVES the only external config dependency (config.py). Post-refactor,
argparse defaults ARE the configuration — there are no external config files to test.

### Config-T1: No config.py Accessible → Module Still Imports

**Purpose:** Verify removal of config import means config.py no longer needed at runtime
**Setup:** Covered by C1 (import test from project root, no special sys.path for config)
**Expected:** `import run_game_data_fetcher; print('OK')` succeeds
**Links to:** REQ-03

### Config-T2: Argparse Defaults Match Former Config Values

**Purpose:** Verify argparse defaults preserve backward-compatible values
**Test:** U2 (test_parse_args_defaults) — season=2025 (was `NFL_SEASON`), current_week=17 (was `CURRENT_NFL_WEEK`)
**Links to:** REQ-02, REQ-08

### Config-T3: Custom Values Override Argparse Defaults

**Purpose:** Verify argparse overrides work correctly
**Test:** C2 (help) + C3/C5 (smoke runs with --season 2024)
**Links to:** REQ-02

### Configuration Test Matrix

| Config Source | Default | Custom | Invalid | Missing |
|---|---|---|---|---|
| --season (was NFL_SEASON) | U2 (2025 ✅) | C5 (--season 2024 ✅) | E5 (non-int → exit ✅) | N/A (argparse provides default) |
| --current-week (was CURRENT_NFL_WEEK) | U2 (17 ✅) | C2 (visible ✅) | variant E5 ✅ | N/A (argparse provides default) |
| config.py (removed entirely) | Config-T1 (absent = correct ✅) | N/A | N/A | Config-T1 (absent = correct ✅) |

---

## Validation Loop Validation

**Validation Date:** 2026-02-19
**Rounds Executed:** 5 rounds
**Issues Found and Fixed:** 1 (Round 2: missing explicit regression suite test C7 — added immediately)
**Exit:** 3 consecutive clean rounds achieved ✅

**Round Summary:**
- Round 1: 0 issues found (count = 1 clean)
- Round 2: 1 issue found — missing C7 (regression suite) → fixed immediately → count reset to 0
- Round 3: 0 issues found (count = 1 clean)
- Round 4: 0 issues found (count = 2 clean)
- Round 5: 0 issues found (count = 3 clean) → PASSED ✅

---

## Next Steps

**This file will be merged into implementation_plan.md during S5.P1.I1:**
- S5.P1.I1 will verify this file exists (MANDATORY check)
- S5.P1.I1 will merge test strategy into "Test Strategy" section of implementation_plan.md
- Implementation tasks will reference these tests

**Test file to create (S6):** `tests/root_scripts/test_run_game_data_fetcher.py`
**Runner to modify (S6):** `run_game_data_fetcher.py`

---

*End of test_strategy.md*
