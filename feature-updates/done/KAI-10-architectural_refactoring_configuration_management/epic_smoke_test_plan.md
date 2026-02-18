## Epic Smoke Test Plan: architectural_refactoring_configuration_management

**Purpose:** Define how to validate the complete KAI-10 epic end-to-end

**Created:** 2026-02-18 (S1 — INITIAL)
**Last Updated:** 2026-02-18 (S3 — updated with concrete scenarios from S2 deep dives)
**Version:** S3 version — will be further updated in S8.P2 after each feature implementation

---

## Epic Success Criteria

**The epic is successful if ALL of the following criteria are met:**

### Criterion 1: Zero CLI Constants in Config Files

✅ **MEASURABLE:** All CLI-configurable constants removed from config/constants files across all 7 scripts.

**Verification:**
```bash
# Check player-data-fetcher config
grep -n "NFL_SEASON\|CURRENT_NFL_WEEK\|ESPN_PLAYER_LIMIT\|REQUEST_TIMEOUT\|RATE_LIMIT_DELAY\|ESPN_PLAYERS_TO_FETCH" player-data-fetcher/config.py

# Check league_helper constants
grep -n "FANTASY_TEAM_NAME\|RECOMMENDATION_COUNT\|MIN_WAIVER_IMPROVEMENT\|NUM_TRADE_RUNNERS_UP\|MIN_TRADE_IMPROVEMENT\|LOGGING_LEVEL" league_helper/constants.py

# Check historical compiler constants
grep -n "REQUEST_TIMEOUT\|RATE_LIMIT_DELAY" historical_data_compiler/constants.py
```
**Expected:** Empty output for all 3 commands.

---

### Criterion 2: Constructor Parameter Pattern Applied

✅ **MEASURABLE:** No internal module imports CLI-configurable values directly from config/constants for runtime use.

**Verification:**
```bash
# Check for surviving direct config imports for CLI-configurable values
grep -rn "from config import.*NFL_SEASON\|from config import.*CURRENT_NFL_WEEK" player-data-fetcher/
grep -rn "from constants import.*FANTASY_TEAM_NAME\|import Constants.*FANTASY_TEAM_NAME" league_helper/
grep -rn "from constants import.*LOGGING_LEVEL\|from constants import.*REQUEST_TIMEOUT" historical_data_compiler/
```
**Expected:** Empty output for all commands (constants removed or non-CLI constants only remain).

---

### Criterion 3: All 7 Runner Scripts Support Universal Args

✅ **MEASURABLE:** Every runner script accepts `--e2e-test` and `--log-level` without error.

**Verification:**
```bash
python run_player_fetcher.py --help | grep -E "e2e-test|log-level"
python run_schedule_fetcher.py --help | grep -E "e2e-test|log-level"
python run_game_data_fetcher.py --help | grep -E "e2e-test|log-level"
python compile_historical_data.py --help | grep -E "e2e-test|log-level"
python run_win_rate_simulation.py --help | grep -E "e2e-test|log-level"
python run_accuracy_simulation.py --help | grep -E "e2e-test|log-level"
python run_league_helper.py --help | grep -E "e2e-test|log-level"
```
**Expected:** Each command shows both `--e2e-test` and `--log-level` in help output. No `--debug` flag (removed per design correction 2026-02-18).

---

### Criterion 4: All 7 E2E Modes Complete in ≤180 Seconds

✅ **MEASURABLE:** Each script's `--e2e-test` mode exits 0 within time budget.

**Verification:** See Part 3 test scenarios. Each script timed individually.

---

### Criterion 5: Graceful Skip Consistent Across Data-Dependent Scripts

✅ **MEASURABLE:** Scripts that depend on local data files (F01, F04, F05, F06, F07) exit 0 with an info log when required files are missing in E2E mode — no traceback.

**Verification:** See Part 4 scenario 8.

---

### Criterion 6: Zero Unit Test Regressions

✅ **MEASURABLE:** All 2,744+ existing unit tests pass after all 7 features are implemented.

**Verification:**
```bash
pytest tests/ -q
```
**Expected:** `2744+ passed, 0 failed`

---

### Criterion 7: Integration Test Framework Operational

✅ **MEASURABLE:** Feature 08's master runner executes and reports pass/fail for all 7 scripts' CLI integration tests.

**Verification:**
```bash
python run_all_integration_tests.py
```
**Expected:** 7/7 passed, exit code 0.

---

## Integration Points Identified

### Integration Point 1: F03 → F01 (fetch_game_data Signature)

**Features Involved:** F01 (refactor_player_data_fetcher), F03 (game_data_fetcher_cli)
**Type:** Computational dependency (function signature)
**Flow:**
- F01 REQ-09: Adds `request_timeout` parameter to `fetch_game_data()` in `player-data-fetcher/game_data_fetcher.py`
- F03 REQ-10: Runner passes `request_timeout=args.request_timeout` to `fetch_game_data()`
- F03 runner cannot be fully implemented until F01 adds the param to `fetch_game_data()`

**Implementation Order:** F01 before F03 (mandatory)

**Test Need:** Verify `fetch_game_data()` accepts `request_timeout` and F03 runner passes it correctly.

---

### Integration Point 2: F08 → F01-F07 (CLI Integration Tests)

**Features Involved:** F08 (integration_test_framework), all 7 features
**Type:** Dependency on all CLI arg names and E2E behaviors
**Flow:**
- F08 creates per-script CLI integration test runners using actual CLI arg names from F01-F07 specs
- F08's master runner (`run_all_integration_tests.py`) invokes all 7 script-level test runners
- F08's S2 is blocked until F01-F07 S2 complete (now done) + S3 + S4

**Test Need:** Verify F08's test runners correctly invoke each script's E2E mode and verify exit codes.

---

### Integration Point 3: Universal Args Consistency (All 7 Scripts)

**Features Involved:** All 7 features
**Type:** Shared interface (universal CLI args)
**Flow:**
- Every runner script must accept `--e2e-test` (flag) and `--log-level` (str, choices=DEBUG/INFO/WARNING/ERROR/CRITICAL)
- No script should have a `--debug` flag (design correction 2026-02-18)
- `--log-level` case-sensitive on F01-F05, F07; F06 normalizes via `type=str.upper` (accepts lowercase too)

**Test Need:** Run `--help` on all 7 and verify consistent universal args presence.

---

### Integration Point 4: E2E Graceful Skip Pattern

**Features Involved:** F01, F04, F05, F06, F07 (data-dependent scripts)
**Type:** Shared behavioral contract
**Flow:**
- F01: Graceful skip if `drafted_data.csv` missing in E2E mode → exit 0
- F04: Graceful skip handled via tempfile (always succeeds in E2E)
- F05: Graceful skip if `sim_data/` or baseline config missing → exit 0
- F06: Graceful skip if `data_path` or baseline missing → exit 0
- F07: Graceful skip if `league_config.json` missing → exit 0
- F02, F03: No skip needed (fetch fresh from APIs)

**Test Need:** Verify consistent exit 0 (no traceback) when data missing in E2E mode across all 5 data-dependent scripts.

---

### Integration Point 5: Argparse Defaults as Single Source of Truth

**Features Involved:** F01, F02, F03 (scripts that previously read NFL_SEASON or CURRENT_NFL_WEEK from config at runtime)
**Type:** Config dependency elimination
**Flow:**
- Pre-refactor: runners fall back to config values for season/week when CLI args omitted
- Post-refactor: hardcoded argparse defaults (2025 / 17) are the only source — config import removed
- Behavioral result identical from user perspective; implementation fundamentally different

**Test Need:** Verify `python <runner>.py` with no args produces same behavior as before (season=2025, week=17), and config import line no longer exists.

---

## Specific Test Scenarios

### Part 1: Import Tests

**Purpose:** Verify all runner scripts load without errors.

#### Scenario 1: Import All Runner Scripts
```bash
python -c "import sys; sys.path.insert(0, '.'); import run_player_fetcher"
python -c "import sys; sys.path.insert(0, '.'); import run_schedule_fetcher"
python -c "import sys; sys.path.insert(0, '.'); import run_game_data_fetcher"
python -c "import sys; sys.path.insert(0, '.'); import run_win_rate_simulation"
python -c "import sys; sys.path.insert(0, '.'); import run_accuracy_simulation"
python -c "import sys; sys.path.insert(0, '.'); import run_league_helper"
python -c "import sys; sys.path.insert(0, 'player-data-fetcher'); import compile_historical_data"
```

**Expected Results:**
✅ No import errors for all 7 scripts
✅ No circular dependency errors
✅ No missing module errors

**Failure Indicators:**
❌ `ModuleNotFoundError` — check sys.path / dependency installation
❌ `ImportError` from config — config import not fully removed

---

### Part 2: Universal Args Entry Point Tests

**Purpose:** Verify all 7 runner scripts accept `--help` and universal args correctly.

#### Scenario 2: All Scripts --help (Universal Args Present)
```bash
python run_player_fetcher.py --help
python run_schedule_fetcher.py --help
python run_game_data_fetcher.py --help
python run_win_rate_simulation.py --help
python run_accuracy_simulation.py --help
python run_league_helper.py --help
```
*(compile_historical_data.py location may differ — check feature 04 implementation)*

**Expected Results:**
✅ Help text displays for all 7 scripts without errors
✅ Both `--e2e-test` and `--log-level` shown in each script's help
✅ No `--debug` flag present (removed per design correction 2026-02-18)
✅ Script-specific args shown (e.g., `--week`, `--season`, `--my-team-name`)

**Failure Indicators:**
❌ `--debug` appears in help → design correction not applied
❌ Missing `--e2e-test` or `--log-level` → universal args not added

---

#### Scenario 3: --log-level Universal Behavior
```bash
python run_player_fetcher.py --log-level DEBUG --e2e-test   # should run and show DEBUG logs
python run_league_helper.py --log-level WARNING --e2e-test  # should run with WARNING level
python run_accuracy_simulation.py --log-level debug --e2e-test  # lowercase accepted (F06 normalizes)
```

**Expected Results:**
✅ DEBUG log output visible when `--log-level DEBUG`
✅ Exit code 0 on all 3 commands
✅ F06 accepts lowercase `debug` (case normalization via `type=str.upper`)

**Failure Indicators:**
❌ Invalid choice error for `debug` (lowercase) in F06 → normalization not applied
❌ No change in log verbosity with DEBUG → wiring to `setup_logger()` missing

---

### Part 3: E2E Execution Tests (with Timing)

**Purpose:** Verify each script's `--e2e-test` mode exits 0 within ≤180s.

#### Scenario 4: Player Fetcher E2E
```bash
time python run_player_fetcher.py --e2e-test
```
**Expected Results:**
✅ Exit code 0
✅ Completes in ≤180s
✅ `E2E test mode` visible in log output (INFO level)

#### Scenario 5: Schedule Fetcher E2E
```bash
time python run_schedule_fetcher.py --e2e-test
```
**Expected Results:**
✅ Exit code 0, ≤180s, only 1 week of data fetched (max_weeks=1)

#### Scenario 6: Game Data Fetcher E2E
```bash
time python run_game_data_fetcher.py --e2e-test
```
**Expected Results:**
✅ Exit code 0, ≤180s, only Week 1 data fetched (weeks=[1])

#### Scenario 7: Win Rate Simulation E2E (data available)
```bash
time python run_win_rate_simulation.py --e2e-test
```
**Expected Results:**
✅ Exit code 0, ≤180s, mode='single', sims=1, workers=1
*(If sim_data/ missing → graceful skip, exit 0 with info message)*

#### Scenario 8: Accuracy Simulation E2E
```bash
time python run_accuracy_simulation.py --e2e-test
```
**Expected Results:**
✅ Exit code 0, ≤180s, 1 parameter × 1 test value evaluated
*(If data or baseline missing → graceful skip, exit 0 with info message)*

#### Scenario 9: League Helper E2E
```bash
time python run_league_helper.py --e2e-test
```
**Expected Results:**
✅ Exit code 0, ≤180s, all 5 modes run via execute_e2e() methods
*(If league_config.json missing → graceful skip, exit 0 with info message)*

#### Scenario 10: Master Integration Test Runner (F08)
```bash
time python run_all_integration_tests.py
```
**Expected Results:**
✅ Reports 7/7 passed, exit code 0
✅ All individual test runners succeed

---

### Part 4: Cross-Feature Integration Tests

**Purpose:** Verify architectural compliance and cross-feature consistency.

#### Scenario 11: E2E Graceful Skip Consistency
Run E2E on data-dependent scripts when data files don't exist (in a temp env or verified-missing state):
```bash
# Assumes league_config.json is missing at expected path
python run_league_helper.py --e2e-test --data-folder /nonexistent/path
python run_win_rate_simulation.py --e2e-test  # if sim_data/ absent
python run_accuracy_simulation.py --e2e-test  # if data absent
```

**Expected Results:**
✅ All 3 exit code 0 (not 1 or 2)
✅ Info-level log message ("skipping") visible in output
✅ No traceback or unhandled exception output

**Failure Indicators:**
❌ Stack trace visible → graceful skip not implemented
❌ Exit code 1 → crash behavior (pre-refactor pattern)

---

#### Scenario 12: F03 → F01 Dependency (fetch_game_data signature)
```bash
python -c "
import sys; sys.path.insert(0, 'player-data-fetcher')
from game_data_fetcher import fetch_game_data
import inspect
sig = inspect.signature(fetch_game_data)
assert 'request_timeout' in sig.parameters, 'request_timeout not in fetch_game_data signature'
print('fetch_game_data signature OK:', sig)
"
```

**Expected Results:**
✅ `request_timeout` in signature
✅ No AssertionError

**Failure Indicators:**
❌ AssertionError → F01 REQ-09 not implemented; F03 cannot pass timeout

---

#### Scenario 13: Config File Compliance (CLI Constants Removed)
```bash
grep -n "NFL_SEASON\|CURRENT_NFL_WEEK\|ESPN_PLAYER_LIMIT\|ESPN_PLAYERS_TO_FETCH\|REQUEST_TIMEOUT\|RATE_LIMIT_DELAY" \
  player-data-fetcher/config.py

grep -n "FANTASY_TEAM_NAME\|RECOMMENDATION_COUNT\|MIN_WAIVER_IMPROVEMENT\|NUM_TRADE_RUNNERS_UP\|MIN_TRADE_IMPROVEMENT\|LOGGING_LEVEL" \
  league_helper/constants.py
```

**Expected Results:**
✅ Empty output for both commands (zero CLI constants remain)

---

#### Scenario 14: Regression — All Unit Tests
```bash
pytest tests/ -q --tb=short
```

**Expected Results:**
✅ 2,744+ passed, 0 failed, 0 errors
✅ All new tests from F05 and F06 (28+ and 12+ new tests) included in count

**Failure Indicators:**
❌ Any failure → regression from architectural change; requires debugging

---

## Update History

| Date | Stage | Feature | What Changed | Why |
|------|-------|---------|--------------|-----|
| 2026-02-18 | S1 | (initial) | Initial plan created | Epic planning based on assumptions and Discovery findings |
| 2026-02-18 | S3 | All (F01-F07) | Substantially rewritten with concrete scenarios from S2 deep dives | S3.P1 — replace placeholder content per guide |
| 2026-02-18 | S3 | All | Removed --debug flag references (design correction 2026-02-18) | Criterion 4 previously referenced --debug which no longer exists |

**Current version is informed by:**
- S1: Initial assumptions and Discovery findings (DISCOVERY.md)
- S2: All 7 feature specs (F01-F07) reviewed; integration points identified; S2.P2 comparison matrix

---

## Execution Checklist (For S9)

**Part 1: Import Tests**
- [ ] Scenario 1: Import All Runner Scripts — {✅ PASSED / ❌ FAILED}

**Part 2: Universal Args Entry Point Tests**
- [ ] Scenario 2: All Scripts --help (universal args present) — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 3: --log-level universal behavior — {✅ PASSED / ❌ FAILED}

**Part 3: E2E Execution Tests**
- [ ] Scenario 4: Player Fetcher E2E — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 5: Schedule Fetcher E2E — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 6: Game Data Fetcher E2E — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 7: Win Rate Simulation E2E — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 8: Accuracy Simulation E2E — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 9: League Helper E2E — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 10: Master Integration Test Runner — {✅ PASSED / ❌ FAILED}

**Part 4: Cross-Feature Integration Tests**
- [ ] Scenario 11: E2E Graceful Skip Consistency — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 12: F03 → F01 Dependency (fetch_game_data) — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 13: Config File Compliance Check — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 14: Regression — All Unit Tests — {✅ PASSED / ❌ FAILED}

**Overall Status:** {ALL PASSED / FAILURES — See details above}

---

## High-Level Test Categories (S8.P2 Additions)

The following categories will have scenarios added during S8.P2 after each feature is implemented, based on actual implementation details:

### Category 1: Error Handling Validation

**What to test:** Invalid arg combinations, conflicting args, API failures in non-E2E mode.
- `--e2e-test` with invalid `--log-level` value (e.g., `--log-level VERBOSE`) → argparse error
- `--historical-season` without `--season` (F03) → check behavior
- `--week` and `--season` both provided to `run_league_helper.py` → config override behavior

### Category 2: Performance Validation

**What to test:** E2E modes under realistic conditions.
- Timed runs when data varies (small vs. large player pool)
- Verify E2E scope reductions are sufficient to stay under 180s budget

### Category 3: Backward Compatibility

**What to test:** No-args invocation identical to pre-refactor behavior.
- `python run_player_fetcher.py` with no args → same behavior as before (same defaults)
- `python run_game_data_fetcher.py` → season=2025, week=17 (argparse defaults match old config defaults)

---

## Notes

**Testing Environment:**
- Python environment with all dependencies installed
- ESPN API access available (real APIs — F01, F02, F03 E2E modes require API access)
- League config file present at expected path for league_helper tests (or graceful skip verified)
- Simulation data files present for F05/F06 E2E (or graceful skip verified)

**Implementation Order Note:**
- F01 must be implemented before F03 (F03 runner depends on F01 REQ-09: `request_timeout` param in `fetch_game_data()`)
- F08 (integration test framework) implemented last — depends on all 7 features being complete

**No --debug flag:**
All references to `--debug` in the S1 version of this plan were incorrect. The design correction (2026-02-18) removed `--debug`. For verbose output use `--e2e-test --log-level DEBUG`.
