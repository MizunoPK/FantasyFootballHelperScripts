# Epic Smoke Test Plan: integrate_new_player_data_into_simulation

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: STAGE 5e (Updated after Feature 01 implementation)**
- Created: 2026-01-02 (Stage 1)
- Last Updated: 2026-01-03 (Stage 5e - After feature_01_win_rate_sim_verification)
- Based on: Feature 01 actual implementation, Stages 2-4 plans
- Quality: CONCRETE - Specific tests based on actual implementation
- Next Update: Stage 5e (after feature_02 and feature_03 implementation)

**Update History:**
- Stage 1: Initial placeholder (assumptions only)
- Stage 4: **MAJOR UPDATE** - Added specific tests, integration points, measurable criteria
- Stage 5e (Feature 01): **IMPLEMENTATION-BASED UPDATE** - Added edge case scenarios, statistical validation, integration details

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

**[UPDATED Stage 5e - feature_01]:** Feature 01 completed this criterion - _parse_players_csv() deleted (SimulatedLeague.py lines 338-361 removed)

---

### Criterion 6: Graceful Error Handling
✅ **MEASURABLE (ADDED Stage 5e - feature_01):** System handles missing or invalid data gracefully
- Missing JSON files: Log warning, continue with other files
- Missing week_N+1 folder: Fallback to projected data, log warning
- Array index out of bounds: Default to 0.0 (no crashes)
- Malformed JSON: Log error, skip file (no crashes)

**Verification:**
```bash
# Run simulation with test scenarios
# Test 1: Remove one JSON file, verify continues
# Test 2: Remove week_18 folder, verify fallback to projected
# Test 3: Use short arrays (< 17 elements), verify defaults to 0.0
# Test 4: Use malformed JSON, verify graceful skip
```

**Why added:** Feature 01 implementation revealed graceful error handling patterns critical for production use. Original epic didn't specify data quality scenarios.

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

### Integration Point 6: Player ID Data Type
**Features Involved:** Features 01 and 02
**Type:** Data structure compatibility
**Description (ADDED Stage 5e - feature_01):**
- Feature 01 implementation revealed: Player IDs are integers (not strings)
- SimulatedLeague.py line 407: `player_id = int(player_dict['id'])`
- JSON files have string IDs ("3918298") but converted to int immediately
- All dictionaries use int keys: `players[player_id]` where player_id is int

**Test Need:** Verify Feature 02 (Accuracy Sim) also uses int player IDs for consistency

**Why added:** Feature 01 tests discovered type mismatch (test initially used string keys, failed with KeyError). Important for Feature 02 to match this pattern.

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
4. **[ADDED Stage 5e - feature_01]:** Perform statistical validation of loaded data

**Expected Results:**
✅ Simulation completes without errors
✅ No CSV file not found errors
✅ JSON files loaded from week_1, week_10, week_17 folders
✅ Week 17 uses week_18 for actual points
✅ **[ADDED Stage 5e - feature_01]:** Non-zero actual_points percentages within expected ranges:
   - QB: 30-40% non-zero (Feature 01 observed 35.0%)
   - RB: 45-55% non-zero (Feature 01 observed 49.4%)
   - WR: 40-50% non-zero (Feature 01 observed 46.9%)
   - TE: 35-45% non-zero (Feature 01 observed 40.8%)
   - K: 75-85% non-zero (Feature 01 observed 81.6%)
   - DST: 75-85% non-zero (Feature 01 observed 81.2%)

**Failure Indicators:**
❌ FileNotFoundError for players.csv → Still trying to load CSV
❌ Simulation crashes → JSON parsing broken
❌ Week 17 uses week_17 for actuals → week_N+1 logic broken
❌ **[ADDED Stage 5e - feature_01]:** >99% zeros → week_N+1 pattern broken (catastrophic bug pattern from historical Feature 02 attempt)

**Why updated:** Feature 01 QC Round 2 performed statistical validation to confirm week_N+1 pattern working correctly. This prevents catastrophic "99.8% zeros" bug pattern. Statistical validation is critical for detecting data loading issues.

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

### Test Scenario 8: Feature 01 Edge Case Handling (ADDED Stage 5e)

**Purpose:** Verify Win Rate Sim handles data quality edge cases gracefully (Feature 01 implementation)

**Added:** Stage 5e (feature_01_win_rate_sim_verification)

**Steps:**
1. Test missing JSON file handling:
   - Remove one position file (e.g., te_data.json) from week_05
   - Run simulation
   - Verify: Log warning "Missing te_data.json", simulation continues, TE players absent from week 5

2. Test missing week_18 folder (week 17 fallback):
   - Temporarily rename week_18 folder
   - Run simulation for week 17
   - Verify: Log warning "Week 18 actual folder not found...Using projected data as fallback", simulation uses projected for actuals

3. Test array index out of bounds:
   - Edit one player's projected_points array to have only 5 elements (< 17)
   - Run simulation for week 10
   - Verify: Player gets 0.0 projected_points for week 10, no IndexError

4. Test malformed JSON:
   - Edit one JSON file to have invalid syntax (missing bracket)
   - Run simulation
   - Verify: Log error, skip file, simulation continues

**Expected Results:**
✅ Missing file: Warning logged, other files still loaded, no crash
✅ Missing week_18: Warning logged, fallback to projected, no crash
✅ Array too short: Default to 0.0, no IndexError
✅ Malformed JSON: Error logged, file skipped, no crash

**Failure Indicators:**
❌ Crashes on missing file → Edge case handling broken
❌ No fallback for missing week_18 → week_N+1 pattern incomplete
❌ IndexError on short array → Bounds checking missing
❌ Crashes on malformed JSON → Error handling missing

**Why added:** Feature 01 enumerated 25 edge cases and implemented graceful handling for all. These 4 tests cover the most critical edge cases that could cause production failures if not handled correctly.

---

### Test Scenario 9: CSV Baseline Comparison (Feature 03 - Optional)

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
| 2026-01-03 | Stage 5e (Feature 01) | **IMPLEMENTATION-BASED UPDATE** | Added tests based on feature_01_win_rate_sim_verification actual implementation |

**Stage 4 changes:**
- Added 8 specific test scenarios (was 4 TBD placeholders)
- Replaced 7 vague success criteria with 5 measurable criteria
- Identified 5 integration points between features
- Added concrete commands and expected outputs for each test
- Documented failure indicators for each test scenario
- Converted high-level categories to concrete guidance

**Stage 5e (Feature 01) changes:**
- **ADDED** Criterion 6: Graceful Error Handling (missing data, malformed JSON, array bounds)
- **ADDED** Integration Point 6: Player ID Data Type (int vs string, discovered via tests)
- **UPDATED** Test Scenario 1: Added statistical validation (non-zero percentages by position)
- **UPDATED** Test Scenario 1: Added catastrophic bug detection (>99% zeros pattern)
- **ADDED** Test Scenario 8: Feature 01 Edge Case Handling (4 critical edge case tests)
- **UPDATED** Criterion 5: Noted Feature 01 completed deprecated code removal

**Rationale for Stage 5e updates:**
- Feature 01 implementation revealed graceful error handling critical for production
- Statistical validation prevents catastrophic "99.8% zeros" bug pattern (historical issue)
- Player ID type mismatch discovered via tests (int keys, not string)
- 25 edge cases enumerated - added 4 most critical to epic test plan
- All updates based on ACTUAL implementation (not specs or assumptions)

**Current version is informed by:**
- Stage 1: Initial assumptions from epic request
- Stage 4: Feature specs and approved implementation plan
- **Stage 5e (Feature 01): Actual implementation of feature_01_win_rate_sim_verification** ← YOU ARE HERE
- Stage 5e (Feature 02): (Pending) Will update after feature_02 implementation
- Stage 5e (Feature 03): (Pending) Will update after feature_03 implementation

**Next update:** Stage 5e after feature_02 and feature_03 complete

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
