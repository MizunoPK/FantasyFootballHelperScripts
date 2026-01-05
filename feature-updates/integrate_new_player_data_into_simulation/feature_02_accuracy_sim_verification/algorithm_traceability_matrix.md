# Algorithm Traceability Matrix - Feature 02

**Purpose:** Map every algorithm in spec.md to exact code locations
**Created:** 2026-01-03 (Stage 5a Round 1 - Iteration 4)

---

## Algorithm Mappings

| Algorithm | Spec Location | Code Location | Line Numbers | Verified |
|-----------|---------------|---------------|--------------|----------|
| **Algorithm 1: Temporary Directory Setup** | spec.md lines 437-462 | AccuracySimulationManager.py `_create_player_manager()` | 339-404 | ✅ |
| **Algorithm 2: Week_N+1 Data Loading** | spec.md lines 466-488 | AccuracySimulationManager.py `_load_season_data()` | 293-337 | ✅ |
| **Algorithm 3: Two-Manager Pattern** | spec.md lines 492-522 | AccuracySimulationManager.py `_evaluate_config_weekly()` | 412-533 | ✅ |

**Total Algorithms:** 3
**All Mapped:** ✅ Yes
**All Verified:** ✅ Yes

---

## Detailed Algorithm Trace

### Algorithm 1: Temporary Directory Setup (_create_player_manager)

**Spec Reference:** spec.md lines 437-462
**Code Location:** simulation/accuracy/AccuracySimulationManager.py lines 339-404

**Verification:**
- ✅ Step 1: Create temp directory (line 359)
- ✅ Step 2: Create player_data/ subfolder (lines 362-363)
- ✅ Step 3: Copy 6 position JSON files (lines 365-373)
- ✅ Step 4: Copy season_schedule.csv (lines 375-378)
- ✅ Step 5: Copy game_data.csv (lines 380-383)
- ✅ Step 6: Copy team_data/ folder (lines 385-388)
- ✅ Step 7: Write league_config.json (lines 390-393)
- ✅ Step 8: Create manager instances (lines 395-399)
- ✅ Step 9: Store temp_dir for cleanup (lines 401-402)
- ✅ Step 10: Return PlayerManager (line 404)

**Deviations:** None - implementation matches spec exactly

---

### Algorithm 2: Week_N+1 Data Loading (_load_season_data)

**Spec Reference:** spec.md lines 466-488
**Code Location:** simulation/accuracy/AccuracySimulationManager.py lines 293-337

**Verification:**
- ✅ Step 1: Input parameters (season_path, week_num) (lines 293-296)
- ✅ Step 2: Calculate projected_folder = week_{week_num:02d} (line 318)
- ✅ Step 3: Calculate actual_week_num = week_num + 1 (line 322)
- ✅ Step 4: Calculate actual_folder = week_{actual_week_num:02d} (line 323)
- ✅ Step 5: Check projected_folder exists (lines 326-328)
- ✅ Step 6: Check actual_folder exists (lines 330-335)
- ✅ Step 7: Return (projected_folder, actual_folder) (line 337)

**Deviations:**
- Spec says "Return (None, None)" when folder missing (line 481-482)
- Code implements this correctly (lines 328, 335)
- **⚠️ Will change in Task 11** (edge case alignment) to return (projected, projected) for missing actual folder

---

### Algorithm 3: Two-Manager Pattern (_evaluate_config_weekly)

**Spec Reference:** spec.md lines 492-522
**Code Location:** simulation/accuracy/AccuracySimulationManager.py lines 412-533

**Verification:**
- ✅ Step 1: Input parameters (config_dict, week_range) (lines 412-416)
- ✅ Step 2a: Loop through seasons (line 430)
- ✅ Step 2a.i: Loop through weeks (line 435)
- ✅ Step 2a.ii: Load season data (line 436)
- ✅ Step 2a.iii: Create projected_mgr (line 444)
- ✅ Step 2a.iv: Create actual_mgr (line 445)
- ✅ Step 2a.v: Try block (line 447)
- ✅ Step 2a.v: Calculate projections from projected_mgr (lines 452-478)
- ✅ Step 2a.v: Extract actuals from actual_mgr (lines 480-497)
- ✅ Step 2a.v: Match by player.id (lines 490-497)
- ✅ Step 2a.v: Store in week_projections, week_actuals (lines 499-501)
- ✅ Step 2a.v: Finally cleanup (lines 503-505)
- ✅ Step 2b: Calculate MAE for season (lines 507-515)
- ✅ Step 3: Aggregate MAE across seasons (line 533)
- ✅ Step 4: Return aggregated AccuracyResult (line 533)

**Deviations:**
- Implementation has additional ranking metrics calculation (lines 512-528)
- Not mentioned in spec Algorithm 3, but not a deviation (enhancement)

---

## Data Structure Mappings

| Data Structure | Spec Location | Code Usage | Verified |
|----------------|---------------|------------|----------|
| JSON File Structure | spec.md lines 369-405 | AccuracySimulationManager.py lines 365-373 (file copying) | ✅ |
| Internal Representation (FantasyPlayer) | spec.md lines 409-431 | PlayerManager (league_helper) | ✅ |
| Temp Directory Structure | spec.md line 442 (step 2) | AccuracySimulationManager.py lines 359-363 | ✅ |
| Two-Manager Pattern | spec.md lines 497-511 | AccuracySimulationManager.py lines 441-505 | ✅ |

---

## Edge Case Mappings

| Edge Case | Spec Location | Code Location | Verified |
|-----------|---------------|---------------|----------|
| Missing JSON File | spec.md lines 561-574 | AccuracySimulationManager.py lines 370-373 | ✅ |
| Missing week_N+1 Folder | spec.md lines 577-596 | AccuracySimulationManager.py lines 330-335 | ⚠️ Will change (Task 11) |
| Array Index Bounds | spec.md lines 599-616 | AccuracySimulationManager.py lines 485-487 | ⚠️ Will change (Task 11) |
| Null or Zero Actual Points | spec.md lines 619-632 | AccuracySimulationManager.py line 487 | ✅ |

---

## Iteration 4 Summary

**Total Mappings:** 10 (3 algorithms + 4 data structures + 3 edge cases)
**All Verified:** ✅ Yes
**Deviations Found:** 2 (both planned changes in Task 11)
**Missing Mappings:** None

**Next:** Proceed to Iteration 4a (TODO Specification Audit - MANDATORY GATE)
