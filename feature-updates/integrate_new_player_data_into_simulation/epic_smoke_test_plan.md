# Epic Smoke Test Plan: integrate_new_player_data_into_simulation

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: STAGE 5e (Updated after feature_01 implementation)**
- Created: 2026-01-01
- Last Updated: 2026-01-02 (Stage 5e - feature_01_win_rate_sim_json_integration)
- Based on: Feature specs (Stages 2-3) + feature_01 actual implementation
- Quality: IMPLEMENTATION-VERIFIED - Tests based on actual code behavior
- Next Update: Stage 5e (after feature_02 implementation)

**Update History:**
- Stage 1: Initial placeholder (assumptions only)
- Stage 4: **MAJOR UPDATE** - Added specific tests, integration points, measurable criteria
- Stage 5e (Feature 1): **IMPLEMENTATION UPDATE** - Added 5 test scenarios based on actual feature_01 code

---

## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: Win Rate Sim Loads JSON Data Successfully
✅ **MEASURABLE:**
- SimulationManager loads historical seasons with JSON files from `simulation/sim_data/{year}/weeks/week_{N:02d}/`
- All 6 position files loaded per week: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
- Simulation completes full execution without errors
- PlayerManager successfully loads from shared_dir/player_data/ structure

**Verification:** Run Win Rate Sim for 2021 season, verify completion without FileNotFoundError or JSON parsing errors

---

### Criterion 2: Accuracy Sim Loads JSON Data Successfully
✅ **MEASURABLE:**
- AccuracySimulationManager loads JSON files from `simulation/sim_data/{year}/weeks/week_{N:02d}/`
- All 6 position files loaded per week (same as Feature 1)
- Accuracy calculations complete for all 4 week ranges (1-5, 6-9, 10-13, 14-17)
- PlayerManager successfully loads from temp_dir/player_data/ structure per config

**Verification:** Run Accuracy Sim for 2021 season weeks 1-17, verify MAE calculations complete for all positions

---

### Criterion 3: Field Structure Handled Correctly
✅ **MEASURABLE:**
- FantasyPlayer.from_json() correctly loads drafted_by (string)
- FantasyPlayer.from_json() correctly loads locked (boolean)
- Both simulations correctly access projected_points[week_num-1] from 17-element array
- Both simulations correctly access actual_points[week_num-1] from 17-element array

**Verification:** Inspect loaded player data, verify field types match spec (string, boolean, float arrays)

---

### Criterion 4: Week 17 Logic Verified
✅ **MEASURABLE (Validation Task):**
- Week 17 evaluation uses week_17 folder's JSON files
- projected_points[16] contains week 17 projected data
- actual_points[16] contains week 17 actual data
- NO special code changes needed (arrays already handle this)

**Verification:** During Accuracy Sim QC (Stage 5c), verify week 17 MAE calculations are correct

---

### Criterion 5: DEF/K Positions Evaluated Correctly
✅ **MEASURABLE (Validation Task):**
- dst_data.json loaded same as other position files
- k_data.json loaded same as other position files
- DEF and K positions included in accuracy calculations
- NO special code needed (handled like other positions)

**Verification:** During Accuracy Sim QC (Stage 5c), verify DEF/K players evaluated in results

---

### Criterion 6: Simulation Functionality Maintained
✅ **MEASURABLE:**
- Win Rate Sim produces valid results (win rate percentages 0-100%)
- Accuracy Sim produces valid results (MAE values > 0)
- Simulation algorithms unchanged (only data source changed from CSV to JSON)
- No regressions in scoring logic or parameter optimization

**Verification:** Compare simulation outputs before/after JSON migration (algorithms should match)

---

## Integration Points Identified

**Note:** Features 1 and 2 are INDEPENDENT subsystems with minimal integration points.

### Integration Point 1: Shared Data Source
**Features Involved:** Feature 1 (Win Rate Sim), Feature 2 (Accuracy Sim)
**Type:** Read from same file location
**Flow:**
- Both features read from `simulation/sim_data/{year}/weeks/week_{N:02d}/`
- Both features expect same 6 JSON files per week
- Both features use same array structure (17 elements, index 0 = Week 1)

**No conflicts** - Features read independently, no shared state

**Test Need:** Verify both simulations can read from same data source without conflicts

---

### Integration Point 2: PlayerManager Dependency
**Features Involved:** Feature 1 (Win Rate Sim), Feature 2 (Accuracy Sim)
**Type:** Shared dependency (but different usage)
**Flow:**
- Feature 1: Creates shared_dir/player_data/, loads once per simulation
- Feature 2: Creates temp_dir/player_data/, loads per config evaluation
- Both use PlayerManager.from_json() for type handling

**No conflicts** - Different directory lifetimes (shared vs temp), both use same PlayerManager interface

**Test Need:** Verify PlayerManager loads JSON correctly for both use cases

---

### Integration Point 3: FantasyPlayer Data Model
**Features Involved:** Feature 1 (Win Rate Sim), Feature 2 (Accuracy Sim)
**Type:** Shared data structure
**Flow:**
- Both features use FantasyPlayer.from_json() to load player data
- Both expect same field types (drafted_by: string, locked: boolean, points arrays: float[17])
- Both rely on FantasyPlayer to handle type conversion

**No conflicts** - Same expectations, same data model

**Test Need:** Verify FantasyPlayer.from_json() works correctly (already tested by Feature 1 research)

---

## Specific Test Scenarios

**These tests MUST be run for epic-level validation:**

### Test Scenario 1: Win Rate Sim JSON Loading (Feature 1)

**Purpose:** Verify Win Rate Sim loads player data from JSON files (not CSV)

**Steps:**
1. Verify JSON data exists: `ls simulation/sim_data/2021/weeks/week_01/*.json` shows 6 files
2. Run Win Rate Sim: `python run_simulation.py --mode win_rate --season 2021 --iterations 100`
3. Verify simulation completes without errors

**Expected Results:**
✅ All 6 JSON files loaded per week (weeks 1-17)
✅ SimulationManager creates shared directory with player_data/ subfolder
✅ Simulation completes successfully (exit code 0)
✅ Results saved to appropriate output location

**Failure Indicators:**
❌ FileNotFoundError → JSON files not in expected location
❌ JSON parsing error → File format incorrect
❌ KeyError → Missing expected field in JSON data
❌ PlayerManager error → player_data/ subfolder not created correctly

**Command to verify:**
```bash
python run_simulation.py --mode win_rate --season 2021 --iterations 100
echo "Exit code: $?"  # Should be 0
```

---

### Test Scenario 2: Accuracy Sim JSON Loading (Feature 2)

**Purpose:** Verify Accuracy Sim loads player data from JSON files (not CSV)

**Steps:**
1. Verify JSON data exists: `ls simulation/sim_data/2021/weeks/week_01/*.json` shows 6 files
2. Run Accuracy Sim: `python run_simulation.py --mode accuracy --season 2021`
3. Verify accuracy calculations complete for all week ranges

**Expected Results:**
✅ All 6 JSON files loaded per week (weeks 1-17)
✅ AccuracySimulationManager creates temp directory per config with player_data/ subfolder
✅ MAE calculations complete for 4 week ranges (1-5, 6-9, 10-13, 14-17)
✅ Results saved to accuracy output location

**Failure Indicators:**
❌ FileNotFoundError → JSON files not in expected location
❌ Week folder not found → week_{N:02d} path incorrect
❌ PlayerManager error → player_data/ subfolder not created correctly
❌ MAE calculation error → Array indexing incorrect

**Command to verify:**
```bash
python run_simulation.py --mode accuracy --season 2021
echo "Exit code: $?"  # Should be 0
```

---

### Test Scenario 3: Field Type Validation (Both Features)

**Purpose:** Verify drafted_by, locked, projected_points, actual_points loaded correctly

**Steps:**
1. Load JSON file: `cat simulation/sim_data/2021/weeks/week_01/qb_data.json`
2. Verify structure: drafted_by (string), locked (boolean), projected_points (array[17])
3. Run Python inspection

**Expected Results:**
✅ drafted_by field is string (not int)
✅ locked field is boolean true/false (not "0"/"1")
✅ projected_points is array with 17 float elements
✅ actual_points is array with 17 float elements
✅ FantasyPlayer.from_json() handles all types correctly

**Failure Indicators:**
❌ Type error → FantasyPlayer.from_json() not handling types correctly
❌ Index error → Array doesn't have 17 elements
❌ Value error → Non-numeric data in points arrays

**Command to verify:**
```python
import json
from pathlib import Path
from utils.FantasyPlayer import FantasyPlayer

# Load JSON file
json_path = Path("simulation/sim_data/2021/weeks/week_01/qb_data.json")
with open(json_path) as f:
    data = json.load(f)

# Check first player
player_dict = data[0]
print(f"drafted_by type: {type(player_dict['drafted_by'])}")  # Should be str
print(f"locked type: {type(player_dict['locked'])}")  # Should be bool
print(f"projected_points length: {len(player_dict['projected_points'])}")  # Should be 17
print(f"actual_points length: {len(player_dict['actual_points'])}")  # Should be 17

# Verify FantasyPlayer loads correctly
player = FantasyPlayer.from_json(player_dict)
print(f"Loaded player: {player.name}, drafted_by={player.drafted_by}, locked={player.locked}")
```

---

### Test Scenario 4: Week 17 Validation (Feature 2 - Accuracy Sim)

**Purpose:** Verify Week 17 scoring uses correct data (validation task, not code change)

**Steps:**
1. Inspect week_17 folder JSON: `cat simulation/sim_data/2021/weeks/week_17/qb_data.json`
2. Verify projected_points[16] and actual_points[16] contain week 17 data
3. Run Accuracy Sim for weeks 14-17 range
4. Verify week 17 included in calculations

**Expected Results:**
✅ week_17 folder contains JSON files
✅ projected_points[16] contains week 17 projected value (not null)
✅ actual_points[16] contains week 17 actual value (not null)
✅ Accuracy Sim includes week 17 in MAE calculation for weeks 14-17 range
✅ NO special week_18 folder logic needed (arrays handle it)

**Failure Indicators:**
❌ projected_points[16] is null → Week 17 data missing
❌ Week 17 not included in calculations → Array indexing error
❌ Week 18 folder required → Spec misunderstanding

**Validation:** During Feature 2 Stage 5c QC, manually verify week 17 MAE is correct

---

### Test Scenario 5: DEF/K Position Validation (Feature 2 - Accuracy Sim)

**Purpose:** Verify DEF and K positions evaluated correctly (validation task, not code change)

**Steps:**
1. Verify dst_data.json and k_data.json exist in week folders
2. Run Accuracy Sim
3. Verify DEF and K positions included in results

**Expected Results:**
✅ dst_data.json loaded (DST position)
✅ k_data.json loaded (K position)
✅ DEF players evaluated in accuracy calculations
✅ K players evaluated in accuracy calculations
✅ NO special handling needed (same as other positions)

**Failure Indicators:**
❌ DEF/K files not loaded → File copying logic missing position
❌ DEF/K not in results → PlayerManager not loading these positions

**Validation:** During Feature 2 Stage 5c QC, verify DEF/K appear in accuracy results

---

### Test Scenario 6: Both Simulations Run Sequentially

**Purpose:** Verify both simulations can run in same environment (minimal integration test)

**Steps:**
1. Run Win Rate Sim: `python run_simulation.py --mode win_rate --season 2021 --iterations 100`
2. Run Accuracy Sim: `python run_simulation.py --mode accuracy --season 2021`
3. Verify no conflicts or errors

**Expected Results:**
✅ Win Rate Sim completes successfully
✅ Accuracy Sim completes successfully
✅ No file conflicts (different temp directories)
✅ No import conflicts (independent modules)

**Failure Indicators:**
❌ Second simulation fails → Shared state conflict
❌ File locked error → Directory cleanup issue

**Command to verify:**
```bash
python run_simulation.py --mode win_rate --season 2021 --iterations 100 && \
python run_simulation.py --mode accuracy --season 2021
echo "Both completed: $?"  # Should be 0
```

---

### Test Scenario 7: Array Indexing Week-Specific Extraction (Feature 1)

**Added:** Stage 5e (feature_01_win_rate_sim_json_integration)

**Purpose:** Verify week-specific data extracted correctly from 17-element arrays using week_num-1 indexing

**Steps:**
1. Load JSON file and verify array structure:
   ```python
   import json
   from pathlib import Path

   json_path = Path("simulation/sim_data/2021/weeks/week_05/qb_data.json")
   with open(json_path) as f:
       data = json.load(f)

   player = data[0]  # First QB
   print(f"Player: {player['name']}")
   print(f"Week 5 projected (index 4): {player['projected_points'][4]}")
   print(f"Week 17 projected (index 16): {player['projected_points'][16]}")
   print(f"Array length: {len(player['projected_points'])}")
   ```

2. Run Win Rate Sim and verify correct week data loaded:
   ```bash
   python run_simulation.py --mode win_rate --season 2021 --iterations 100
   ```

3. Verify logs show correct array indexing (week_num - 1)

**Expected Results:**
✅ Arrays have exactly 17 elements (indices 0-16)
✅ Week 1 data at index 0
✅ Week 5 data at index 4
✅ Week 17 data at index 16
✅ _parse_players_json() correctly extracts week-specific values
✅ No IndexError exceptions

**Failure Indicators:**
❌ IndexError → Array doesn't have 17 elements or wrong indexing
❌ Wrong values → Off-by-one error in indexing (week_num instead of week_num-1)

**Why added:** Implementation revealed `week_num - 1` indexing pattern in _parse_players_json() (SimulatedLeague.py:364-371). Stage 4 plan assumed JSON loading worked but didn't test array extraction logic explicitly.

---

### Test Scenario 8: Week Data Caching Optimization (Feature 1)

**Added:** Stage 5e (feature_01_win_rate_sim_json_integration)

**Purpose:** Verify all 17 weeks pre-loaded into memory cache (optimization maintained)

**Steps:**
1. Enable debug logging to see cache operations
2. Run Win Rate Sim:
   ```bash
   python run_simulation.py --mode win_rate --season 2021 --iterations 100
   ```

3. Check logs for caching messages:
   - Should see: "Cached week 1: {count} players"
   - Should see: "Cached week 17: {count} players"
   - Should see 17 cache messages total (one per week)

**Expected Results:**
✅ All 17 weeks pre-loaded before simulation starts
✅ _preload_all_weeks() called during initialization
✅ week_data_cache contains all 17 weeks
✅ Optimization reduces file reads from ~340 to 17

**Failure Indicators:**
❌ Weeks loaded on-demand → Caching not working
❌ Multiple reads per week → Cache not being used
❌ Performance regression → Caching optimization lost

**Why added:** Implementation uses _preload_all_weeks() (SimulatedLeague.py:269-297) to cache all 17 weeks for performance. Stage 4 plan didn't mention this optimization. Critical to verify it's maintained.

---

### Test Scenario 9: Missing JSON File Error Handling (Feature 1)

**Added:** Stage 5e (feature_01_win_rate_sim_json_integration)

**Purpose:** Verify simulation continues gracefully when individual JSON files missing

**Steps:**
1. Create test scenario (backup files first):
   ```bash
   cd simulation/sim_data/2021/weeks/week_03/
   mv k_data.json k_data.json.backup  # Temporarily remove kicker data
   ```

2. Run Win Rate Sim:
   ```bash
   python run_simulation.py --mode win_rate --season 2021 --iterations 100
   ```

3. Check logs for warning message:
   - Should see: "Missing k_data.json in .../week_03"
   - Should NOT see ERROR or exception

4. Restore file:
   ```bash
   mv k_data.json.backup k_data.json
   ```

**Expected Results:**
✅ Simulation completes successfully (doesn't crash)
✅ Warning logged: `self.logger.warning(f"Missing {position_file}...")`
✅ Other positions (QB, RB, WR, TE, DST) load correctly
✅ Week 3 loads with 5 positions instead of 6
✅ Exit code 0 (success)

**Failure Indicators:**
❌ FileNotFoundError exception → Error handling not working
❌ Simulation crashes → Not gracefully handling missing files
❌ No warning logged → Logging pattern not followed

**Why added:** Implementation has explicit error handling for missing JSON files (SimulatedLeague.py:232-235, 342-345). Logs warning and continues. Stage 4 plan said "Stage 5e will add error handling tests" - this fulfills that.

---

### Test Scenario 10: Shared Directory player_data Subfolder (Feature 1)

**Added:** Stage 5e (feature_01_win_rate_sim_json_integration)

**Purpose:** Verify shared directory created with player_data/ subfolder (PlayerManager requirement)

**Steps:**
1. Run Win Rate Sim with verbose logging:
   ```bash
   python run_simulation.py --mode win_rate --season 2021 --iterations 10
   ```

2. Check temp directory structure during simulation:
   - Find temp directory (check logs or /tmp)
   - Verify structure:
     ```
     shared_data/
       player_data/
         qb_data.json
         rb_data.json
         wr_data.json
         te_data.json
         k_data.json
         dst_data.json
       league_config.json
       season_schedule.csv
       game_data.csv
       team_data/
     ```

**Expected Results:**
✅ shared_data/ directory created (not per-team directories)
✅ player_data/ subfolder exists inside shared_data/
✅ All 6 JSON files copied to player_data/
✅ Other files copied to shared_data/ root (config, schedule, game_data, team_data)
✅ Optimization: 1 directory instead of 10 per-team directories

**Failure Indicators:**
❌ player_data/ subfolder missing → PlayerManager will fail (hardcoded path)
❌ JSON files in wrong location → PlayerManager can't find them
❌ Multiple directories created → Optimization lost

**Why added:** Implementation creates shared_dir/player_data/ structure (SimulatedLeague.py:222-236). PlayerManager hardcodes this path (PlayerManager.py:327). Critical requirement not explicitly tested in Stage 4 plan.

---

### Test Scenario 11: Validation - Season Data Valid Player Count (Feature 1)

**Added:** Stage 5e (feature_01_win_rate_sim_json_integration)

**Purpose:** Verify SimulationManager._validate_season_data() counts valid players correctly from JSON

**Steps:**
1. Check validation logic manually:
   ```python
   from simulation.win_rate.SimulationManager import SimulationManager
   from pathlib import Path

   manager = SimulationManager()
   season_path = Path("simulation/sim_data/2021")

   # This runs validation internally
   seasons = manager.discover_historical_seasons(season_path.parent)
   print(f"Valid seasons found: {len(seasons)}")
   print(f"Season 2021 validated: {'2021' in seasons}")
   ```

2. Verify validation counts players with `projected_points[0] > 0` and `drafted_by == ''`

**Expected Results:**
✅ Validation reads week_01 JSON files (not CSV)
✅ Counts only undrafted players with positive week 1 projections
✅ Season 2021 passes validation (has sufficient valid players)
✅ No FileNotFoundError during validation

**Failure Indicators:**
❌ Validation still looking for CSV files → Code not updated
❌ Wrong player count → Validation logic incorrect
❌ Season fails validation → JSON data structure issue

**Why added:** Implementation updated _validate_season_data() to parse JSON files and count valid players (SimulationManager.py:231-273). Stage 4 plan doesn't test validation logic explicitly. Important for ensuring seasons are validated correctly before simulation.

---

## High-Level Test Categories

**These categories have been built up through Stage 4 (specs) and Stage 5e (implementation):**

### Category 1: JSON File Loading
**What to test:** All 6 position files loaded correctly per week
**Stage 4 scenarios:** Test Scenarios 1, 2, 3
**Stage 5e added (Feature 1):** Test Scenario 9 (missing file error handling), Test Scenario 11 (validation logic)

---

### Category 2: Array Indexing
**What to test:** Week-specific data extracted correctly from arrays
**Stage 4 scenarios:** Test Scenarios 3, 4
**Stage 5e added (Feature 1):** Test Scenario 7 (week-specific extraction with week_num-1 indexing)

---

### Category 3: PlayerManager Integration
**What to test:** player_data/ subfolder created, JSON loaded correctly
**Stage 4 scenarios:** Test Scenarios 1, 2
**Stage 5e added (Feature 1):** Test Scenario 10 (shared_dir/player_data/ structure requirement)

---

### Category 4: Simulation Results Consistency
**What to test:** Results match pre-JSON baseline (no algorithm regressions)
**Stage 4 scenarios:** Test Scenario 6
**Stage 5e added (Feature 1):** Test Scenario 8 (week data caching optimization maintained)

---

### Category 5: Validation Tasks (Week 17/18, DEF/K)
**What to test:** Week 17 and DEF/K work correctly (no code changes needed)
**Stage 4 scenarios:** Test Scenarios 4, 5
**Stage 5e added (Feature 1):** None (these remain QC validation tasks for feature_02)

---

## Update Log

| Date | Stage | What Changed | Why |
|------|-------|--------------|-----|
| 2026-01-01 | Stage 1 | Initial plan created | Epic planning - assumptions only |
| 2026-01-01 | Stage 4 | **MAJOR UPDATE** | Based on feature specs (Stages 2-3) |
| 2026-01-02 | Stage 5e (Feature 1) | Added 5 test scenarios based on actual implementation | feature_01 implementation revealed array indexing, caching, error handling, shared_dir structure, and validation logic not explicitly tested in Stage 4 |

**Stage 4 changes:**
- Added 6 specific test scenarios (was TBD)
- Replaced vague success criteria with 6 measurable criteria
- Identified 3 integration points between features
- Added concrete commands and expected outputs
- Documented failure indicators for each test
- Clarified Week 17/18 and DEF/K are VALIDATION tasks (not code changes)

**Stage 5e (Feature 1) changes:**
- **Test Scenario 7:** Array indexing week-specific extraction (week_num-1 pattern)
- **Test Scenario 8:** Week data caching optimization (all 17 weeks pre-loaded)
- **Test Scenario 9:** Missing JSON file error handling (logs warning, continues)
- **Test Scenario 10:** Shared directory player_data/ subfolder structure
- **Test Scenario 11:** Validation logic for counting valid players from JSON
- Total new scenarios: 5 (covering implementation details not in specs)

**Current version is informed by:**
- Stage 1: Initial assumptions from epic request
- Stage 4: Feature specs and approved implementation plan
- **Stage 5e (Feature 1): Actual feature_01 implementation code** ← YOU ARE HERE
- Stage 5e (Feature 2): (Pending) Will update after feature_02 implementation

**Next update:** Stage 5e after feature_02 completes (will add Accuracy Sim-specific tests)

---

**END OF EPIC SMOKE TEST PLAN (Updated through Stage 5e - Feature 1)**
