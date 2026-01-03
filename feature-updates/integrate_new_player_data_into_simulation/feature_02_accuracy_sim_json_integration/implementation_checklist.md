# Feature 02: Accuracy Simulation JSON Integration - Implementation Checklist

**Created:** 2026-01-02 (Stage 5b Step 2)
**Purpose:** Real-time verification that all spec requirements are implemented
**Instructions:** Check off requirements AS YOU IMPLEMENT (not batched at end)

---

## Requirements from Spec.md

### Objective Requirements

- [x] 1.1: Update Accuracy Simulation subsystem to load player data from position-specific JSON files (Task 1-4)
- [x] 1.2: Maintain same accuracy evaluation functionality (no algorithm changes) (Validation)

### Scope Requirements

- [x] 2.1: Update AccuracySimulationManager.py to copy JSON files instead of CSV files (Task 1, 1a, 2)
- [x] 2.2: Update ParallelAccuracyRunner.py to copy JSON files instead of CSV files (Task 3, 3a, 4)
- [x] 2.3: Create player_data/ subfolder in temp directories (Task 2, 4)
- [x] 2.4: Handle new JSON file structure (6 position files per week) (Task 2, 4)
- [x] 2.5: Maintain all existing accuracy calculation logic (no changes) (Validation)

### Components Affected - AccuracySimulationManager.py

- [x] 3.1: Modify _load_season_data() to return week_folder path instead of CSV file paths (Task 1)
- [x] 3.2: Return (week_folder, week_folder) tuple for compatibility (Task 1)
- [x] 3.3: Update caller line 414 to NOT use .parent (Task 1a)
- [x] 3.4: Modify _create_player_manager() to create player_data/ subfolder (Task 2)
- [x] 3.5: Copy 6 JSON files from week_folder to player_data/ (Task 2)
- [x] 3.6: Log warning for missing JSON files (Task 2)
- [x] 3.7: Continue copying other files even if one JSON missing (graceful degradation) (Task 2)
- [x] 3.8: Copy season-level files to temp_dir root (unchanged) (Task 2)
- [x] 3.9: Create league_config.json in temp_dir root (unchanged) (Task 2)
- [x] 3.10: Return PlayerManager instance (unchanged) (Task 2)

### Components Affected - ParallelAccuracyRunner.py

- [x] 4.1: Modify _load_season_data() module function to return week_folder path (Task 3)
- [x] 4.2: Return (week_folder, week_folder) tuple for compatibility (Task 3)
- [x] 4.3: Update caller line 119 to NOT use .parent (Task 3a)
- [x] 4.4: Modify _create_player_manager() module function to create player_data/ subfolder (Task 4)
- [x] 4.5: Copy 6 JSON files from week_folder to player_data/ (Task 4)
- [x] 4.6: Log warning for missing JSON files (Task 4)
- [x] 4.7: Continue copying other files even if one JSON missing (Task 4)
- [x] 4.8: Copy season-level files to temp_dir root (unchanged) (Task 4)
- [x] 4.9: Create league_config.json in temp_dir root (unchanged) (Task 4)
- [x] 4.10: Return PlayerManager instance (unchanged) (Task 4)

### Implementation Details - Temp Directory Structure

- [x] 5.1: Create temp_dir/player_data/ subfolder (Task 2, 4)
- [x] 5.2: Copy qb_data.json to player_data/ (Task 2, 4)
- [x] 5.3: Copy rb_data.json to player_data/ (Task 2, 4)
- [x] 5.4: Copy wr_data.json to player_data/ (Task 2, 4)
- [x] 5.5: Copy te_data.json to player_data/ (Task 2, 4)
- [x] 5.6: Copy k_data.json to player_data/ (Task 2, 4)
- [x] 5.7: Copy dst_data.json to player_data/ (Task 2, 4)
- [x] 5.8: Log warning if any position file missing (Task 2, 4)
- [x] 5.9: Continue with other files even if one missing (Task 2, 4)

### Implementation Details - Error Handling

- [x] 6.1: Return (None, None) if week_folder doesn't exist (Task 1, 3)
- [x] 6.2: Log warning for missing JSON files, continue (Task 2, 4)
- [x] 6.3: Copy season files with exists() checks (Task 2, 4)

### Week 17/18 Logic (Validation)

- [x] 7.1: Verify week_17 folder's JSON files are loaded correctly (Task 6) - Verified in smoke testing
- [x] 7.2: Verify projected_points[16] contains week 17 projected data (Task 6) - Verified in smoke testing
- [x] 7.3: Verify actual_points[16] contains week 17 actual data (Task 6) - Verified in smoke testing
- [x] 7.4: Verify MAE calculations for week 17 are correct (Task 6) - Verified in smoke testing

### DEF/K Position Evaluation (Validation)

- [x] 8.1: Verify dst_data.json loaded correctly (Task 7) - Verified in smoke testing (32 DST players)
- [x] 8.2: Verify k_data.json loaded correctly (Task 7) - Verified in smoke testing (38 K players)
- [x] 8.3: Verify DEF players included in accuracy calculations (Task 7) - Verified in smoke testing
- [x] 8.4: Verify K players included in accuracy calculations (Task 7) - Verified in smoke testing

### Test Fixtures

- [x] 9.1: Update test fixtures to create 6 JSON files per week (not CSV) (Task 5)
- [x] 9.2: JSON files have required structure (17-element arrays) (Task 5)
- [x] 9.3: Test data covers all 6 positions (QB, RB, WR, TE, K, DST) (Task 5)
- [x] 9.4: Fixtures create week_folder structure (not individual CSV files) (Task 5)

### Documentation

- [x] 10.1: Update _load_season_data() docstring in AccuracySimulationManager.py (Task 1)
- [x] 10.2: Update _create_player_manager() docstring in AccuracySimulationManager.py (Task 2)
- [x] 10.3: Update _load_season_data() docstring in ParallelAccuracyRunner.py (Task 3)
- [x] 10.4: Update _create_player_manager() docstring in ParallelAccuracyRunner.py (Task 4)

---

## Summary

**Total Requirements:** 60
**Completed:** 60 (100%) ✅
**Remaining:** 0

**Progress by Category:**
- Objective: 2/2 ✓ (100%)
- Scope: 5/5 ✓ (100%)
- AccuracySimulationManager: 10/10 ✓ (100%)
- ParallelAccuracyRunner: 10/10 ✓ (100%)
- Temp Directory: 9/9 ✓ (100%)
- Error Handling: 3/3 ✓ (100%)
- Week 17/18: 4/4 ✓ (100% - Verified in smoke testing)
- DEF/K: 4/4 ✓ (100% - Verified in smoke testing)
- Test Fixtures: 4/4 ✓ (100%)
- Documentation: 4/4 ✓ (100%)

**Implementation Status:** COMPLETE ✅
- All code changes implemented (Tasks 1-5)
- All validation requirements verified (Tasks 6-7 in smoke testing)
- All unit tests passing (2463/2463 - 100%)
- All integration tests passing (12/12 - 100%)
- 100% of spec requirements met

_This checklist will be updated in REAL-TIME during implementation_

