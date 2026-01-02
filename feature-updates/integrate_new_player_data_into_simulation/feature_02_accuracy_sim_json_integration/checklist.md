# Feature 02: Accuracy Simulation JSON Integration - Planning Checklist

**Status:** ✅ ALL QUESTIONS RESOLVED (leveraging Feature 1 findings)
**Created:** 2026-01-01 (Stage 2 Deep Dive)
**Last Updated:** 2026-01-02 (Stage 5d - updated based on feature_01 implementation)

---

## Resolution Summary

All questions answered by leveraging Feature 1's codebase investigation. No additional research needed.

**See:**
- `research/ACCURACY_SIM_DISCOVERY.md` - Accuracy Sim specific findings
- `research/CODEBASE_INVESTIGATION_FINDINGS.md` - Feature 1's shared findings

---

## Resolved Questions

### ✅ Question 1: Temp Directory Structure

**Answer:** Create `temp_dir/player_data/` subfolder with 6 JSON files

**Evidence:**
- Same as Feature 1 - PlayerManager hardcodes `data_folder/player_data/` path
- PlayerManager.py:327 confirms this requirement

**Impact:** _create_player_manager() must create player_data/ subfolder

---

### ✅ Question 2: File Copying Approach

**Answer:** Copy 6 JSON files instead of glob copying all `.csv` files

**Current logic:** Lines 343-346 copy all files matching `.csv` extension
**New logic:** Explicit list of 6 position JSON files

**Impact:** Replace file.suffix == '.csv' with explicit position file list

---

### ✅ Question 3: Week 17/18 Folder Logic

**Answer:** Use week_17 folder only - arrays contain all data

**Investigation findings:**
- JSON arrays already encode week 17 data: `projected_points[16]` and `actual_points[16]`
- Week 18 folder exists for data completeness but not used during evaluation
- Current code loops weeks 1-17 (AccuracySimulationManager.py:303)

**Conclusion:** Epic request is VALIDATION task, not code change
- Will verify week 17 works correctly during Stage 5c QC
- No special week_18 logic needed

**Impact:** Standard JSON loading - no special handling required

---

### ✅ Question 4: DEF/K Evaluation

**Answer:** Same handling as other positions - no special code needed

**Investigation findings:**
- DEF = `dst_data.json`, K = `k_data.json` (two of the 6 position files)
- No special handling in Accuracy Sim code
- PlayerManager loads all 6 positions equally

**Conclusion:** Epic request is VALIDATION task, not code change
- Will verify DEF/K work correctly during Stage 5c QC
- No special code needed

**Impact:** Standard JSON loading - DEF/K handled automatically

---

### ✅ Question 5: Array Indexing

**Answer:** Index 0 = Week 1, Index 16 = Week 17 (same as Feature 1)

**Evidence:**
- Feature 1 confirmed via json_exporter.py:328
- Arrays have 17 elements (REGULAR_SEASON_WEEKS = 17)

**Impact:** No indexing logic in Accuracy Sim (PlayerManager handles arrays)

---

### ✅ Question 6: Field Type Handling

**Answer:** NO conversion needed - FantasyPlayer.from_json() handles types correctly

**Evidence:**
- Feature 1 verified FantasyPlayer.from_json() handles:
  - `locked`: boolean loaded directly
  - `drafted_by`: string loaded directly
- Same PlayerManager code path

**Impact:** No type conversion logic needed in Accuracy Sim

---

### ✅ Question 7: Error Handling for Missing Files

**[UPDATED based on feature_01 implementation - 2026-01-02]**

**Answer:** Return None if week_folder missing, calling code logs warnings for missing individual files

**Current behavior:**
- Returns (None, None) if CSV files don't exist
- Calling code checks and skips week

**New behavior:**
- Return None if week_folder doesn't exist
- Calling code actively logs warnings for missing individual JSON files (not PlayerManager)
- Logging pattern from feature_01: `self.logger.warning(f"Missing {position_file} in {week_folder}")`
- Same graceful degradation

**Update from feature_01 implementation:**
Feature_01 showed that the calling code should proactively log warnings (SimulatedLeague.py:235),
not assume PlayerManager will handle logging. This provides better debugging visibility.

**Impact:** Minimal changes to error handling logic, with explicit warning logging

---

## Implementation Checklist

**Changes Required:**
- [x] Confirm temp directory structure (player_data/ subfolder)
- [x] Confirm file copying approach (explicit JSON file list)
- [x] Confirm Week 17/18 logic (validation task, not code change)
- [x] Confirm DEF/K handling (validation task, not code change)
- [x] Confirm array indexing (PlayerManager handles it)
- [x] Confirm field type handling (no conversion needed)
- [x] Confirm error handling (same pattern as CSV)

**Ready for spec.md finalization:** ✅

---

## Cross-Feature Alignment

**Alignment with Feature 1:**
- ✅ Same PlayerManager JSON loading approach
- ✅ Same player_data/ subfolder requirement
- ✅ Same field type handling (no conversion)
- ✅ Same error handling pattern

**Key differences:**
- Feature 1: Pre-loads and caches week data (needs JSON parsing)
- Feature 2: Loads on-demand (just file copying, PlayerManager parses)

**Differences are INTENTIONAL** - different use cases require different approaches

---

**Next Step:** Update lessons_learned.md, then proceed to Phase 4 & 5
