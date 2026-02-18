## Feature Spec: integration_test_framework

**Status:** APPROVED — Gate 3 passed 2026-02-18
**Last Updated:** 2026-02-18

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

Wave 3 — Create 7 CLI integration test runners + master runner + INTEGRATION_TESTING_GUIDE.md. Requires all 7 feature specs complete.

**Key scope items:**
- Create 5 new CLI test files:
  - test_player_fetcher_cli.py
  - test_schedule_fetcher_cli.py
  - test_game_data_fetcher_cli.py
  - test_historical_compiler_cli.py
  - test_league_helper_cli.py
- Enhance 2 existing simulation test files:
  - test_simulation_integration.py (add TestWinRateSimulationCLI class)
  - test_accuracy_simulation_integration.py (add TestAccuracySimulationCLI class)
- Create master runner: run_all_integration_tests.py
- Create INTEGRATION_TESTING_GUIDE.md (~300 lines, 5 sections)
- Each test runner validates: exit codes + specific outcomes (log messages, output files, data values)
- 3-5 argument combinations tested per script
- All tests use --e2e-test mode (≤180 seconds per script)

### Relevant Discovery Decisions

- **Solution Approach:** Integration tests use subprocess to invoke each runner with CLI args; assert exit code 0 and specific outcomes
- **Key Constraints:** All 7 feature specs must be complete before this feature's S2; INTEGRATION_TESTING_GUIDE.md is this feature's documentation deliverable
- **Dependencies:** Wave 3 — depends on all 7 feature specs (Features 01-07) being complete
- **Timeout policy:** Tests warn but do not fail on >180s (network variability — user answer from Discovery)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Documentation as separate feature? | No — INTEGRATION_TESTING_GUIDE.md is this feature's deliverable | Create guide in S7.P3 as part of this feature |
| Testing strictness for E2E timeout | Warn only (network variability) | Tests warn but don't fail on >180s timeout |

---

## Requirements

### REQ-01: CLI Test File Locations

**Source:** DISCOVERY.md + S2 research (existing test patterns)

All 5 new CLI test files must be created in `tests/integration/` (not a new directory):

| New File | Script Tested | Existing File in tests/integration/ |
|----------|--------------|--------------------------------------|
| `tests/integration/test_player_fetcher_cli.py` | `run_player_fetcher.py` | `test_data_fetcher_integration.py` (different — uses direct import) |
| `tests/integration/test_schedule_fetcher_cli.py` | `run_schedule_fetcher.py` | `test_schedule_fetcher_integration.py` (different — tests logging, not CLI args) |
| `tests/integration/test_game_data_fetcher_cli.py` | `run_game_data_fetcher.py` | None |
| `tests/integration/test_historical_compiler_cli.py` | `compile_historical_data.py` | `test_historical_data_compiler_integration.py` (different — mocks sys.argv) |
| `tests/integration/test_league_helper_cli.py` | `run_league_helper.py` | `test_league_helper_integration.py` (different — uses direct import) |

**Rationale:** `tests/integration/test_schedule_fetcher_integration.py` establishes the subprocess.run() pattern in tests/integration/. The 5 new files follow this same pattern without conflicting.

The 2 enhanced files already exist:
- `tests/integration/test_simulation_integration.py` → add `TestWinRateSimulationCLI` class
- `tests/integration/test_accuracy_simulation_integration.py` → add `TestAccuracySimulationCLI` class

---

### REQ-02: CLI Test Implementation Pattern

**Source:** DISCOVERY.md + S2 research (test_schedule_fetcher_integration.py pattern)

All 7 CLI test runners must use subprocess to invoke runner scripts:

```python
import subprocess, sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent

result = subprocess.run(
    [sys.executable, str(project_root / "run_SCRIPT.py"), "--e2e-test", ...extra_args],
    capture_output=True,
    text=True,
    timeout=180
)
```

**Mandatory assertions for all tests:**
- `assert result.returncode == 0` for ALL 7 scripts (strict — including API-dependent scripts F02, F03)
- Assert NO traceback in stderr: `assert "Traceback" not in result.stderr`

**Note on API-dependent scripts (F02, F03):** Tests assert `returncode == 0`. If the ESPN API is unavailable during testing, these tests will fail. This is intentional — tests require a working network environment. The test environment must have ESPN API access to pass.

**Outcome assertions (in addition to exit code):**
- When script exits 0 AND produces output files: assert output file exists
- When script exits 0 via graceful skip: assert expected skip message in stderr

**Timeout handling (RESOLVED Q3 — Option A):** Tests must pass `timeout=180` to subprocess.run(). If timeout is exceeded, the test emits a warning but does not fail:
```python
try:
    result = subprocess.run([...], timeout=180, capture_output=True, text=True)
except subprocess.TimeoutExpired:
    import warnings
    warnings.warn("E2E test exceeded 180s timeout — skipping assertions", RuntimeWarning)
    return  # Test passes with warning
```

---

### REQ-03: TestPlayerFetcherCLI — test_player_fetcher_cli.py

**Source:** F01 spec (REQ-01, REQ-11) + DISCOVERY.md

**Script:** `run_player_fetcher.py`
**Test class:** `TestPlayerFetcherCLI`

**Argument combinations to test (3-5):**

| Test Method | Args | Expected Outcome |
|-------------|------|-----------------|
| `test_e2e_baseline` | `--e2e-test` | exit 0; no Traceback |
| `test_e2e_debug_log_level` | `--e2e-test --log-level DEBUG` | exit 0; no Traceback |
| `test_e2e_specific_week` | `--e2e-test --week 1` | exit 0; no Traceback |
| `test_e2e_graceful_skip_no_data` | `--e2e-test` (no drafted_data.csv) | exit 0; assert "Skipping" OR success in stderr |
| `test_help_shows_all_args` | `--help` | exit 0; assert all 17 arg names present in stdout |

**F01 E2E behavior (REQ-11):** espn_player_limit=100, graceful skip if drafted_data.csv missing (exit 0).

**Key assertion — help text:**
```python
assert "--e2e-test" in result.stdout
assert "--log-level" in result.stdout
assert "--week" in result.stdout
assert "--season" in result.stdout
assert "--my-team-name" in result.stdout
```

---

### REQ-04: TestScheduleFetcherCLI — test_schedule_fetcher_cli.py

**Source:** F02 spec (REQ-01, REQ-04) + DISCOVERY.md

**Script:** `run_schedule_fetcher.py`
**Test class:** `TestScheduleFetcherCLI`

**F02 E2E behavior:** max_weeks=1 (fetches 1 week only). Requires ESPN API access (exit 0 expected — network required).

**Argument combinations to test (3-5):**

| Test Method | Args | Expected Outcome |
|-------------|------|-----------------|
| `test_e2e_baseline` | `--e2e-test` | exit 0; no Traceback |
| `test_e2e_debug_log_level` | `--e2e-test --log-level DEBUG` | exit 0; no Traceback |
| `test_e2e_custom_season` | `--e2e-test --season 2024` | exit 0; no Traceback |
| `test_e2e_custom_output_path` | `--e2e-test --output-path /tmp/test_sched.csv` | exit 0; assert output file exists at /tmp/test_sched.csv |
| `test_help_shows_all_args` | `--help` | exit 0; assert --e2e-test, --log-level, --season, --output-path in stdout |

---

### REQ-05: TestGameDataFetcherCLI — test_game_data_fetcher_cli.py

**Source:** F03 spec (REQ-01, E2E behavior) + DISCOVERY.md

**Script:** `run_game_data_fetcher.py`
**Test class:** `TestGameDataFetcherCLI`

**F03 E2E behavior:** Fetches from API directly, removes os.chdir(). CLI args: --e2e-test, --log-level, --request-timeout, --historical-season (8 total). Requires ESPN API access (exit 0 expected — network required).

**Argument combinations to test (3-5):**

| Test Method | Args | Expected Outcome |
|-------------|------|-----------------|
| `test_e2e_baseline` | `--e2e-test` | exit 0; no Traceback |
| `test_e2e_debug_log_level` | `--e2e-test --log-level DEBUG` | exit 0; no Traceback |
| `test_e2e_with_timeout` | `--e2e-test --request-timeout 60` | exit 0; no Traceback |
| `test_e2e_historical_season` | `--e2e-test --historical-season 2024` | exit 0; no Traceback |
| `test_help_shows_all_args` | `--help` | exit 0; assert --e2e-test, --log-level, --request-timeout, --historical-season in stdout |

---

### REQ-06: TestHistoricalCompilerCLI — test_historical_compiler_cli.py

**Source:** F04 spec (REQ-01, E2E behavior) + DISCOVERY.md

**Script:** `compile_historical_data.py`
**Test class:** `TestHistoricalCompilerCLI`

**F04 E2E behavior:** Uses tempfile for output (always succeeds — no API dependency). 8 total args: --year, --verbose (preserved), --enable-log-file, --output-dir, --e2e-test, --log-level, --timeout, --rate-limit-delay.

**Argument combinations to test (3-5):**

| Test Method | Args | Expected Outcome |
|-------------|------|-----------------|
| `test_e2e_baseline` | `--e2e-test` | **exit 0** (always — tempfile); no Traceback |
| `test_e2e_debug_log_level` | `--e2e-test --log-level DEBUG` | exit 0; no Traceback |
| `test_e2e_specific_year` | `--e2e-test --year 2024` | exit 0; no Traceback |
| `test_e2e_custom_timeout` | `--e2e-test --timeout 120` | exit 0; no Traceback |
| `test_help_shows_all_args` | `--help` | exit 0; assert --e2e-test, --log-level, --timeout, --rate-limit-delay in stdout |

**Note:** F04 uses tempfile for E2E output, so `assert result.returncode == 0` (not [0,1]). This is the only script where exact exit code 0 is always expected.

---

### REQ-07: TestLeagueHelperCLI — test_league_helper_cli.py

**Source:** F07 spec (REQ-01, REQ-07) + DISCOVERY.md

**Script:** `run_league_helper.py`
**Test class:** `TestLeagueHelperCLI`

**F07 E2E behavior:** Runs all 5 interactive modes via `execute_e2e()`, no user prompts, ≤180s total. Graceful skip if `league_config.json` not found (exit 0 + info log). CLI args: --e2e-test, --log-level, --my-team-name, --recommendation-count, --min-waiver-improvement, --num-runners-up, --min-trade-improvement, --data-folder, --mode, --week, --season, --enable-log-file (12 total).

**Argument combinations to test (3-5):**

| Test Method | Args | Expected Outcome |
|-------------|------|-----------------|
| `test_e2e_baseline` | `--e2e-test` | exit 0 (graceful skip if no data, or success); no Traceback |
| `test_e2e_debug_log_level` | `--e2e-test --log-level DEBUG` | exit 0; no Traceback |
| `test_e2e_custom_team_name` | `--e2e-test --my-team-name "Test Team"` | exit 0; no Traceback |
| `test_e2e_graceful_skip` | `--e2e-test --data-folder /tmp/nonexistent` | exit 0; assert "league_config.json not found" OR "Skipping" in stderr |
| `test_help_shows_all_args` | `--help` | exit 0; assert --e2e-test, --log-level, --mode, --data-folder, --my-team-name in stdout |

---

### REQ-08: TestWinRateSimulationCLI — added to test_simulation_integration.py

**Source:** F05 spec (E2E behavior) + DISCOVERY.md

**Script:** `run_win_rate_simulation.py`
**Test class:** `TestWinRateSimulationCLI` (new class added to existing file)

**F05 E2E behavior:** Forces mode=single, sims=1, workers=1. Graceful skip if simulation data missing (exit 0). 11 total args (9 existing + --e2e-test + --log-level).

**Argument combinations to test (3-5):**

| Test Method | Args | Expected Outcome |
|-------------|------|-----------------|
| `test_e2e_baseline` | `--e2e-test` | exit 0 (graceful skip or success); no Traceback |
| `test_e2e_debug_log_level` | `--e2e-test --log-level DEBUG` | exit 0; no Traceback |
| `test_e2e_warning_log_level` | `--e2e-test --log-level WARNING` | exit 0; no Traceback |
| `test_help_shows_e2e_flag` | `--help` | exit 0; assert --e2e-test and --log-level in stdout |

**Location:** Add `TestWinRateSimulationCLI` class at the END of the existing `tests/integration/test_simulation_integration.py` file. Do NOT modify existing test classes.

---

### REQ-09: TestAccuracySimulationCLI — added to test_accuracy_simulation_integration.py

**Source:** F06 spec (E2E behavior) + DISCOVERY.md

**Script:** `run_accuracy_simulation.py`
**Test class:** `TestAccuracySimulationCLI` (new class added to existing file)

**F06 E2E behavior:** Graceful skip if data missing (exit 0). Normalizes --log-level to uppercase via `type=str.upper` (accepts both `debug` and `DEBUG`). 11 total args (10 existing + --e2e-test).

**Argument combinations to test (3-5):**

| Test Method | Args | Expected Outcome |
|-------------|------|-----------------|
| `test_e2e_baseline` | `--e2e-test` | exit 0 (graceful skip or success); no Traceback |
| `test_e2e_uppercase_log_level` | `--e2e-test --log-level DEBUG` | exit 0; no Traceback |
| `test_e2e_lowercase_log_level` | `--e2e-test --log-level debug` | exit 0; no Traceback (F06 normalizes to uppercase) |
| `test_help_shows_e2e_flag` | `--help` | exit 0; assert --e2e-test in stdout |

**Location:** Add `TestAccuracySimulationCLI` class at the END of the existing `tests/integration/test_accuracy_simulation_integration.py` file. Do NOT modify existing test classes.

---

### REQ-10: run_all_integration_tests.py — Master Runner

**Source:** DISCOVERY.md + user answer (7/7 pass required)

**Location:** Project root (`run_all_integration_tests.py`)

**Purpose:** Run all 7 CLI integration test files and report pass/fail. Exits 0 if all 7 pass, exits 1 if any fail.

**The 7 test files it runs:**
1. `tests/integration/test_player_fetcher_cli.py`
2. `tests/integration/test_schedule_fetcher_cli.py`
3. `tests/integration/test_game_data_fetcher_cli.py`
4. `tests/integration/test_historical_compiler_cli.py`
5. `tests/integration/test_league_helper_cli.py`
6. `tests/integration/test_simulation_integration.py::TestWinRateSimulationCLI`
7. `tests/integration/test_accuracy_simulation_integration.py::TestAccuracySimulationCLI`

**Implementation approach:** The master runner invokes pytest as a subprocess for each test file (or all at once), capturing results. Example:
```python
import subprocess, sys
from pathlib import Path

project_root = Path(__file__).parent

TEST_FILES = [
    "tests/integration/test_player_fetcher_cli.py",
    "tests/integration/test_schedule_fetcher_cli.py",
    "tests/integration/test_game_data_fetcher_cli.py",
    "tests/integration/test_historical_compiler_cli.py",
    "tests/integration/test_league_helper_cli.py",
    "tests/integration/test_simulation_integration.py::TestWinRateSimulationCLI",
    "tests/integration/test_accuracy_simulation_integration.py::TestAccuracySimulationCLI",
]

def main():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"] + TEST_FILES,
        capture_output=False  # Show output in real time
    )
    if result.returncode == 0:
        print("\n✅ All 7/7 integration test suites passed.")
    else:
        print("\n❌ One or more integration test suites failed.")
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
```

**Requirements:**
- REQ-10a: Script runs all 7 test files when invoked as `python run_all_integration_tests.py`
- REQ-10b: Reports pass/fail count
- REQ-10c: Exit code 0 if all pass, exit code 1 if any fail
- REQ-10d: Optional `--verbose` flag to show detailed output

---

### REQ-11: INTEGRATION_TESTING_GUIDE.md

**Source:** DISCOVERY.md + user answer (INTEGRATION_TESTING_GUIDE.md is this feature's documentation deliverable)

**Location:** `docs/testing/INTEGRATION_TESTING_GUIDE.md`
**Target length:** ~300 lines
**Created:** In S7.P3 (after implementation is complete), NOT in S5/S6

**5 required sections:**

**Section 1: Overview**
- What integration tests validate (E2E CLI invocation, not unit behavior)
- Relationship to unit tests (separate concerns — unit tests in tests/, integration here)
- When to run (after implementing any F01-F07 feature, before merging)

**Section 2: Running Individual Tests**
- How to run each of the 7 test files individually with pytest
- Example commands for each script
- Expected output format

**Section 3: Running the Master Runner**
- `python run_all_integration_tests.py`
- What 7/7 pass means
- How to interpret pass/fail output

**Section 4: Understanding Test Outputs**
- Exit code meanings (0=success, 1=graceful API failure or skip)
- Graceful skip behavior (F01, F05, F06, F07 — missing data files → exit 0)
- Network-dependent tests (F02, F03 — may fail if ESPN API down)
- Timeout warnings vs failures

**Section 5: Troubleshooting**
- API unavailable: test returns exit 1 (acceptable)
- Missing data files: graceful skip (exit 0)
- Timeout exceeded: warning only
- Test fails with Traceback: indicates bug in runner script

---

### REQ-12: No Modification to Existing Test Classes

**Source:** Derived from zero-regression requirement + research showing existing integration tests are complete

When adding `TestWinRateSimulationCLI` to `test_simulation_integration.py` and `TestAccuracySimulationCLI` to `test_accuracy_simulation_integration.py`, existing test classes must NOT be modified:

- `test_simulation_integration.py`: Existing classes (`TestConfigGeneratorIntegration`, `TestSimulationManagerIntegration`, `TestParallelLeagueRunnerIntegration`, `TestResultsManagerIntegration`, `TestConfigPerformanceIntegration`) remain unchanged.
- `test_accuracy_simulation_integration.py`: All existing test classes remain unchanged.

New classes are APPENDED at the end of each file.

---

## Acceptance Criteria

- [ ] `python run_all_integration_tests.py` exits 0 (7/7 pass)
- [ ] `pytest tests/integration/test_player_fetcher_cli.py -v` runs 5 tests without error
- [ ] `pytest tests/integration/test_schedule_fetcher_cli.py -v` runs 5 tests without error
- [ ] `pytest tests/integration/test_game_data_fetcher_cli.py -v` runs 5 tests without error
- [ ] `pytest tests/integration/test_historical_compiler_cli.py -v` runs 5 tests without error
- [ ] `pytest tests/integration/test_league_helper_cli.py -v` runs 5 tests without error
- [ ] `pytest tests/integration/test_simulation_integration.py::TestWinRateSimulationCLI -v` runs 4 tests
- [ ] `pytest tests/integration/test_accuracy_simulation_integration.py::TestAccuracySimulationCLI -v` runs 4 tests
- [ ] No existing tests in test_simulation_integration.py or test_accuracy_simulation_integration.py broken
- [ ] `docs/testing/INTEGRATION_TESTING_GUIDE.md` exists (~300 lines, 5 sections)
- [ ] `pytest tests/` (full suite) still passes 100% (all existing tests unaffected)

---

## Open Scope Questions

See `checklist.md` for resolved/pending decisions.

---

## Files to Create/Modify

| File | Change Type | Complexity |
|------|-------------|------------|
| `tests/integration/test_player_fetcher_cli.py` | Create (new) | Low |
| `tests/integration/test_schedule_fetcher_cli.py` | Create (new) | Low |
| `tests/integration/test_game_data_fetcher_cli.py` | Create (new) | Low |
| `tests/integration/test_historical_compiler_cli.py` | Create (new) | Low |
| `tests/integration/test_league_helper_cli.py` | Create (new) | Low |
| `tests/integration/test_simulation_integration.py` | Modify (append class) | Low |
| `tests/integration/test_accuracy_simulation_integration.py` | Modify (append class) | Low |
| `run_all_integration_tests.py` | Create (new) | Low |
| `docs/testing/INTEGRATION_TESTING_GUIDE.md` | Create (new, S7.P3) | Medium |

**Total: 9 files (8 test/runner + 1 doc)**
