## Epic Smoke Test Plan: architectural_refactoring_configuration_management

**Purpose:** Define how to validate the complete KAI-10 epic end-to-end

**Created:** 2026-02-18 (S1 — INITIAL, will be updated in S4)
**Last Updated:** 2026-02-18 (S1)

> ⚠️ **NOTE:** This is the initial S1 plan based on assumptions. It will be substantially updated in S4 (Epic Testing Strategy) after S2 deep dives are complete, and further updated during S8.P2 after each feature implementation.

---

## Epic Success Criteria

**The epic is successful if:**

1. All 7 runner scripts expose every configurable constant exclusively as CLI arguments — zero CLI-configurable constants remain in config/constants files
   - Verified by: `grep -r "CURRENT_NFL_WEEK\|NFL_SEASON\|ESPN_PLAYER_LIMIT" player-data-fetcher/config.py` returns empty

2. All 7 runner scripts use the constructor parameter pattern — no config module imports for CLI-configurable values in internal modules
   - Verified by: code inspection and unit tests passing

3. All 7 runner scripts support `--e2e-test` mode completing successfully in ≤180 seconds
   - Verified by: timed execution of each script's E2E mode

4. All 7 runner scripts support `--debug` and `--log-level` with consistent behavior (DEBUG logging + reduced data scope)
   - Verified by: behavioral testing with --debug flag

5. All 7 CLI integration test runners exist and pass via master runner
   - Verified by: `python run_all_integration_tests.py` reports 7/7 passed, exit code 0

6. All 2,744+ existing unit tests continue to pass (100% pass rate — zero regressions)
   - Verified by: `pytest tests/` reports 2,744+ passed, 0 failed

7. INTEGRATION_TESTING_GUIDE.md created covering all 7 scripts and usage patterns
   - Verified by: file exists at `docs/testing/INTEGRATION_TESTING_GUIDE.md` with ≥300 lines

**Epic is considered SUCCESSFUL when ALL criteria above are met.**

---

## Update History

**Track when and why this plan was updated:**

| Date | Stage | Feature | What Changed | Why |
|------|-------|---------|--------------|-----|
| 2026-02-18 | S1 | (initial) | Initial plan created | Epic planning based on assumptions and Discovery findings |

**Current version is informed by:**
- S1: Initial assumptions and Discovery findings (DISCOVERY.md)

---

## Test Scenarios

> ⚠️ **NOTE:** These scenarios are initial assumptions. Specific commands, file paths, and data verification steps will be updated in S4 and S8.P2 based on actual implementation.

**Instructions for Agent:**
- Execute EACH scenario listed below
- Verify ACTUAL DATA VALUES (not just "file exists")
- Document results in S9

---

### Part 1: Epic-Level Import Tests

**Purpose:** Verify all runner scripts and internal modules can be imported together

**Scenario 1: Import All Runner Scripts**
```bash
python -c "import run_player_fetcher; import run_schedule_fetcher; import compile_historical_data"
python -c "import run_game_data_fetcher; import run_win_rate_simulation; import run_accuracy_simulation; import run_league_helper"
```

**Expected Result:**
- No import errors
- No circular dependency errors
- All runner scripts load successfully

---

### Part 2: Epic-Level Entry Point Tests

**Purpose:** Verify all 7 runner scripts accept --help and universal args without crashing

**Scenario 2: All Scripts --help**
```bash
python run_player_fetcher.py --help
python run_schedule_fetcher.py --help
python run_game_data_fetcher.py --help
python compile_historical_data.py --help
python run_win_rate_simulation.py --help
python run_accuracy_simulation.py --help
python run_league_helper.py --help
```

**Expected Result:**
- Help text displays for all 7 scripts
- All expected options shown (script-specific + universal: --debug, --e2e-test, --log-level)
- No crashes or errors

**Scenario 3: Universal Args on All Scripts**
```bash
python run_player_fetcher.py --log-level DEBUG --help
python run_league_helper.py --log-level INFO --help
```

**Expected Result:**
- --log-level accepted on all scripts
- --debug accepted on all scripts
- Consistent behavior across all 7

---

### Part 3: Epic End-to-End Execution Tests

**Purpose:** Execute complete E2E workflows with real APIs, verifying ≤180s completion

**Scenario 4: Player Fetcher E2E**
```bash
time python run_player_fetcher.py --week 1 --espn-player-limit 100 --e2e-test
```

**Expected Result:**
- Exits 0 in <180s
- Player data fetched successfully
- No errors in output

**Scenario 5: League Helper E2E (all 5 modes)**
```bash
time python run_league_helper.py --mode draft --e2e-test
```

**Expected Result:**
- Exits 0 in <180s
- All 5 modes complete without user prompts
- No exceptions

**Scenario 6: Master Integration Test Runner**
```bash
python run_all_integration_tests.py
```

**Expected Result:**
- Reports 7/7 passed
- Exit code 0
- All individual test runners succeed

{Additional E2E scenarios to be added in S4 and S8.P2}

---

### Part 4: Cross-Feature Integration Tests

**Purpose:** Test that the constructor parameter pattern works consistently across all features

**Scenario 7: Regression Test — All Unit Tests**
```bash
pytest tests/ -q
```

**Expected Result:**
- 2,744+ passed, 0 failed
- No regressions from architectural changes

**Scenario 8: Config File Compliance Check**
```bash
grep -r "CURRENT_NFL_WEEK\|NFL_SEASON\|ESPN_PLAYER_LIMIT\|REQUEST_TIMEOUT\|RATE_LIMIT_DELAY" \
  player-data-fetcher/config.py \
  historical_data_compiler/constants.py \
  schedule-data-fetcher/ 2>/dev/null
```

**Expected Result:**
- Empty output (zero CLI constants remain in config/constants files)

{Integration scenarios between specific features to be added in S8.P2}

---

## High-Level Test Categories

**Instructions for Agent:**
- These categories are FLEXIBLE — create specific scenarios as needed during S8.P2
- Base scenarios on ACTUAL implementation (not assumptions)

---

### Category 1: Error Handling Validation

**What to test:** All 7 runner scripts handle errors gracefully

**Agent will create scenarios for:**
- Invalid argument combinations
- Missing required files (league config, data files)
- Conflicting arguments (--debug with --log-level WARNING)
- E2E mode timeout behavior

---

### Category 2: Performance Validation

**What to test:** E2E modes complete within ≤180 second limit

**Agent will create scenarios for:**
- Each of the 7 scripts timed in E2E mode
- Debug mode doesn't degrade below 180s limit
- No significant performance regressions from refactoring

---

### Category 3: Architectural Compliance

**What to test:** Constructor parameter pattern applied consistently

**Agent will create scenarios for:**
- Verify no `from config import` statements for CLI-configurable values in internal modules
- Verify settings flow correctly from runner → main() → internal modules
- Verify argparse defaults are single source of truth

---

## Execution Checklist (For S9)

**Part 1: Import Tests**
- [ ] Scenario 1: Import All Runner Scripts — {✅ PASSED / ❌ FAILED}

**Part 2: Entry Point Tests**
- [ ] Scenario 2: All Scripts --help — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 3: Universal Args on All Scripts — {✅ PASSED / ❌ FAILED}

**Part 3: E2E Execution Tests**
- [ ] Scenario 4: Player Fetcher E2E — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 5: League Helper E2E — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 6: Master Integration Test Runner — {✅ PASSED / ❌ FAILED}
- [ ] {Additional scenarios added in S4/S8.P2...}

**Part 4: Cross-Feature Integration Tests**
- [ ] Scenario 7: Regression Test (all unit tests) — {✅ PASSED / ❌ FAILED}
- [ ] Scenario 8: Config File Compliance Check — {✅ PASSED / ❌ FAILED}
- [ ] {Additional integration scenarios added in S8.P2...}

**Overall Status:** {ALL PASSED / FAILURES — See details above}

---

## Notes

**Testing Environment:**
- Python environment with all dependencies installed
- ESPN API access available (real APIs, not mocked)
- League config file present at expected path for league_helper tests
- Data files present at expected paths for simulation tests

**Known Issues:**
- None (initial plan)

**Important:** This plan is substantially incomplete at S1. The key additions expected in later stages:
- S4: Specific data verification checks for each script's output
- S8.P2 (Feature 01): Settings dict validation scenarios
- S8.P2 (Feature 07): League helper interactive mode automation details
- S8.P2 (Feature 08): Integration test framework validation steps
