# Epic Smoke Test Plan: integrate_new_player_data_into_simulation

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: STAGE 4 (Updated after deep dives)**
- Created: 2026-01-02 (Stage 1)
- Last Updated: 2026-01-03 (Stage 4 - MAJOR UPDATE)
- Based on: Feature specs from Stages 2-3, approved implementation plan
- Quality: CONCRETE - Specific tests based on actual feature designs
- Next Update: Stage 5e (after each feature implementation - will add more tests)

**Update History:**
- Stage 1: Initial placeholder (assumptions only)
- Stage 4: **MAJOR UPDATE** - Added specific tests, integration points, measurable criteria
- Stage 5e: (Pending) Will update after each feature implementation

---

## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: Win Rate Simulation Runs Successfully with JSON
✅ **MEASURABLE:** Run Win Rate Simulation with JSON data for weeks 1, 10, and 17
- No FileNotFoundError for players.csv or players_projected.csv
- Simulation completes without errors
- Week 17 data loaded from week_18 for actuals

**Verification:**
```bash
python run_win_rate_simulation.py
# Check logs for successful completion
# Verify no CSV file errors
```

---

### Criterion 2: Accuracy Simulation Runs Successfully with JSON
✅ **MEASURABLE:** Run Accuracy Simulation with JSON data for weeks 1, 10, and 17
- PlayerManager loads JSON files correctly
- Simulation completes without errors
- Week 17 data loaded from week_18 for actuals
- MAE scores calculated successfully

**Verification:**
```bash
python run_accuracy_simulation.py
# Check logs for successful completion
# Verify MAE output generated
```

---

### Criterion 3: All Unit Tests Pass
✅ **MEASURABLE:** Complete test suite passes with 100% pass rate
- All 2,200+ tests pass
- Exit code 0
- No test failures related to JSON migration

**Verification:**
```bash
python tests/run_all_tests.py
echo "Exit code: $?"  # Should be 0
```

---

### Criterion 4: Documentation Updated
✅ **MEASURABLE:** All documentation reflects JSON structure
- simulation/README.md updated (CSV references removed, JSON docs added)
- All docstrings updated (6 locations across 5 files)
- Migration guide added to README

**Verification:**
```bash
# Verify zero player CSV references
grep -r "players\.csv\|players_projected\.csv" simulation/
# Should return 0 results (or only game_data.csv, season_schedule.csv)
```

---

### Criterion 5: Deprecated Code Removed
✅ **MEASURABLE:** All deprecated CSV loading code removed
- SimulatedLeague._parse_players_csv() method deleted
- No calls to _parse_players_csv() in codebase

**Verification:**
```bash
# Check method doesn't exist
grep -r "_parse_players_csv" simulation/
# Should return 0 results
```

---

## Integration Points Identified

### Integration Point 1: JSON Loading Patterns
**Features Involved:** Features 01 and 02
**Type:** Architectural difference (intentional)
**Description:**
- Feature 01 (Win Rate Sim): Direct JSON parsing via _parse_players_json()
- Feature 02 (Accuracy Sim): PlayerManager delegation (temporary directory pattern)
- Both patterns work with same JSON files

**Test Need:** Verify BOTH patterns work correctly with JSON data

---

### Integration Point 2: Edge Case Alignment
**Features Involved:** Features 01 and 02
**Type:** Behavioral consistency
**Description:**
- Feature 02 Requirement 7 aligns edge case handling with Feature 01
- Missing week_N+1 folder: Both fallback to projected data
- Array index out of bounds: Both default to 0.0

**Test Need:** Verify both simulations handle edge cases consistently

---

### Integration Point 3: Week 17 Logic
**Features Involved:** Features 01, 02, and 03
**Type:** Data loading dependency
**Description:**
- Both simulations must load week_17 for projected, week_18 for actual
- Feature 03 tests this logic in both simulations

**Test Need:** Verify Week 17 uses week_18 folder for actuals in both sims

---

### Integration Point 4: Testing Dependencies
**Features Involved:** All features (01, 02, 03)
**Type:** Sequential dependency
**Description:**
- Feature 03 depends on Features 01 AND 02 being complete
- Feature 03 tests both simulations end-to-end
- All features use same test weeks (1, 10, 17)

**Test Need:** Verify Features 01 and 02 complete before Feature 03 runs

---

### Integration Point 5: Documentation Consistency
**Features Involved:** All features (01, 02, 03)
**Type:** Documentation updates
**Description:**
- Features 01 and 02 update docstrings in their respective modules
- Feature 03 comprehensively updates simulation/README.md
- All must align on JSON structure description

**Test Need:** Verify zero CSV references across all simulation files

---

## Specific Test Scenarios

**These tests MUST be run for epic-level validation:**

### Test Scenario 1: Win Rate Sim JSON Loading (Feature 01)

**Purpose:** Verify Win Rate Simulation loads JSON data correctly

**Steps:**
1. Run Win Rate Simulation for weeks 1, 10, and 17
   ```bash
   python run_win_rate_simulation.py
   ```
2. Check logs for JSON file loading
3. Verify no FileNotFoundError for CSV files

**Expected Results:**
✅ Simulation completes without errors
✅ No CSV file not found errors
✅ JSON files loaded from week_1, week_10, week_17 folders
✅ Week 17 uses week_18 for actual points

**Failure Indicators:**
❌ FileNotFoundError for players.csv → Still trying to load CSV
❌ Simulation crashes → JSON parsing broken
❌ Week 17 uses week_17 for actuals → week_N+1 logic broken

---

### Test Scenario 2: Accuracy Sim JSON Loading (Feature 02)

**Purpose:** Verify Accuracy Simulation loads JSON via PlayerManager correctly

**Steps:**
1. Run Accuracy Simulation for weeks 1, 10, and 17
   ```bash
   python run_accuracy_simulation.py
   ```
2. Check logs for PlayerManager JSON loading
3. Verify MAE scores calculated

**Expected Results:**
✅ Simulation completes without errors
✅ PlayerManager loads JSON from player_data/ temp directories
✅ MAE scores output generated
✅ Week 17 uses week_18 for actual points

**Failure Indicators:**
❌ FileNotFoundError → PlayerManager can't find JSON files
❌ Empty player list → JSON files not copied to temp directory
❌ MAE calculation fails → Array extraction broken

---

### Test Scenario 3: Edge Case Consistency (Features 01 & 02)

**Purpose:** Verify both simulations handle edge cases consistently

**Steps:**
1. Test missing week_N+1 folder scenario
2. Test array index out of bounds scenario
3. Compare behavior between Win Rate and Accuracy sims

**Expected Results:**
✅ Both sims fallback to projected data when actual folder missing
✅ Both sims default to 0.0 when array too short
✅ Consistent error messages and logging

**Failure Indicators:**
❌ Different behaviors → Edge case alignment (Req 7) not implemented
❌ Crashes instead of graceful fallback → Edge case handling broken

---

### Test Scenario 4: Week 17 Specific Verification (All Features)

**Purpose:** Verify Week 17 uses week_17 for projected, week_18 for actual in both sims

**Steps:**
1. Run both simulations for week 17 only
2. Inspect loaded data (projected vs actual folders)
3. Verify actual_points extracted from week_18 data

**Expected Results:**
✅ Win Rate Sim: _preload_week_data() uses week_17 and week_18
✅ Accuracy Sim: _load_season_data(17) returns (week_17, week_18)
✅ Both extract actual_points[16] from week_18 data

**Failure Indicators:**
❌ Uses week_17 for both → week_N+1 logic not working
❌ Index error on actual_points → Array structure wrong

---

### Test Scenario 5: Complete Unit Test Suite (All Features)

**Purpose:** Verify all 2,200+ unit tests pass after JSON migration

**Steps:**
1. Run complete test suite
   ```bash
   python tests/run_all_tests.py
   ```
2. Verify exit code 0
3. Check for any JSON-related test failures

**Expected Results:**
✅ 100% test pass rate (2,200+ tests)
✅ Exit code 0
✅ No FileNotFoundError in test logs
✅ Simulation integration tests pass

**Failure Indicators:**
❌ Exit code 1 → Tests failing
❌ FileNotFoundError → Tests still expecting CSV files
❌ JSON parsing errors → Test data structure wrong

---

### Test Scenario 6: Documentation Verification (Feature 03)

**Purpose:** Verify zero player CSV references remain and documentation complete

**Steps:**
1. Search for player CSV references
   ```bash
   grep -r "players\.csv\|players_projected\.csv" simulation/
   ```
2. Verify simulation/README.md updated
3. Verify all docstrings updated

**Expected Results:**
✅ grep returns 0 player CSV references
✅ simulation/README.md has JSON structure section
✅ simulation/README.md has CSV → JSON migration guide
✅ All docstrings updated (6 locations verified)

**Failure Indicators:**
❌ grep finds player CSV references → Documentation not updated
❌ README missing JSON docs → Incomplete documentation update
❌ Docstrings still reference CSV → Missed update locations

---

### Test Scenario 7: Deprecated Code Removal (Feature 01)

**Purpose:** Verify _parse_players_csv() method deleted and no calls remain

**Steps:**
1. Search for deprecated method
   ```bash
   grep -r "_parse_players_csv" simulation/
   ```
2. Verify method no longer in SimulatedLeague.py
3. Verify no code calls the deprecated method

**Expected Results:**
✅ grep returns 0 results (method deleted)
✅ SimulatedLeague.py does not contain _parse_players_csv definition
✅ No calls to deprecated method found

**Failure Indicators:**
❌ Method still exists → Not deleted as specified
❌ Calls to method found → Code still using deprecated path

---

### Test Scenario 8: CSV Baseline Comparison (Feature 03 - Optional)

**Purpose:** Compare JSON results to CSV baseline if available

**Steps:**
1. Run simulations with JSON data
2. Compare results to saved CSV baseline outputs (if exist)
3. Verify key metrics match (win rates, MAE scores)

**Expected Results:**
✅ Win rates within reasonable tolerance of CSV baseline
✅ MAE scores within reasonable tolerance of CSV baseline
✅ Results verify "same functionality" claim

**Failure Indicators:**
❌ Results significantly differ → Regression from CSV baseline
❌ No baseline exists → Skip this test (acceptable)

**Note:** This test is optional if CSV baseline outputs don't exist

---

## High-Level Test Categories

**Agent will create additional scenarios for these categories during Stage 5e:**

### Category 1: JSON Data Structure Validation
**What to test:** JSON files correctly structured and parsed
**Known test points:**
- 6 position files per week (QB, RB, WR, TE, K, DST)
- 17-element arrays for projected_points, actual_points
- Array indexing with [week_num - 1]

**Stage 5e will add:** Specific tests for each position file after implementation

---

### Category 2: Error Handling
**What to test:** Graceful degradation when data missing or invalid
**Known error scenarios:**
- Missing JSON file (log warning, continue)
- Missing week_N+1 folder (fallback to projected)
- Array index out of bounds (default to 0.0)

**Stage 5e will add:** Specific error scenarios discovered during implementation

---

### Category 3: Performance
**What to test:** JSON loading doesn't significantly slow down simulations
**Known performance points:**
- Loading 6 JSON files per week
- Parsing JSON vs CSV performance
- Memory usage with JSON structures

**Stage 5e will add:** Performance benchmarks after implementation

---

### Category 4: Regression Prevention
**What to test:** JSON migration doesn't break existing functionality
**Known regression risks:**
- Simulation logic changes
- Scoring calculation changes
- Week 17 edge case breaks

**Stage 5e will add:** Regression tests after implementation

---

## Update Log

| Date | Stage | What Changed | Why |
|------|-------|--------------|-----|
| 2026-01-02 | Stage 1 | Initial plan created | Epic planning - assumptions only |
| 2026-01-03 | Stage 4 | **MAJOR UPDATE** | Based on feature specs (Stages 2-3) |

**Stage 4 changes:**
- Added 8 specific test scenarios (was 4 TBD placeholders)
- Replaced 7 vague success criteria with 5 measurable criteria
- Identified 5 integration points between features
- Added concrete commands and expected outputs for each test
- Documented failure indicators for each test scenario
- Converted high-level categories to concrete guidance

**Current version is informed by:**
- Stage 1: Initial assumptions from epic request
- **Stage 4: Feature specs and approved implementation plan** ← YOU ARE HERE
- Stage 5e: (Pending) Will update after each feature implementation

**Next update:** Stage 5e after each feature completes (will add implementation-specific tests)

---

**Epic Implementation Order (from Stage 3):**
1. Features 01 and 02 in parallel (independent)
2. Feature 03 sequential (depends on both 01 and 02)

**Test Execution Order:**
1. Test Scenario 5 (unit tests) - Run first to catch any obvious breaks
2. Test Scenarios 1-2 (individual simulations) - Verify each sim independently
3. Test Scenarios 3-4 (integration) - Verify sims work together correctly
4. Test Scenarios 6-7 (documentation/cleanup) - Verify completeness
5. Test Scenario 8 (baseline comparison) - Optional final verification

---

*This test plan will be updated in Stage 5e after each feature implementation with additional integration tests and implementation-specific scenarios.*
