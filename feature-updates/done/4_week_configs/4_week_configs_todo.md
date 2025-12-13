# 4 Week Configs - Implementation TODO

## Iteration Progress Tracker

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 |

**Current Iteration:** COMPLETE (24/24)

---

## Protocol Execution Tracker

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [ ]1 [ ]2 [ ]3 [ ]8 [ ]9 [ ]10 [ ]15 [ ]16 |
| Algorithm Traceability | 4, 11, 19 | [ ]4 [ ]11 [ ]19 |
| End-to-End Data Flow | 5, 12 | [ ]5 [ ]12 |
| Skeptical Re-verification | 6, 13, 22 | [ ]6 [ ]13 [ ]22 |
| Integration Gap Check | 7, 14, 23 | [ ]7 [ ]14 [ ]23 |
| Fresh Eyes Review | 17, 18 | [ ]17 [ ]18 |
| Edge Case Verification | 20 | [ ]20 |
| Test Coverage Planning | 21 | [ ]21 |
| Implementation Readiness | 24 | [ ]24 |

---

## Verification Summary

- Iterations completed: 24/24
- Requirements from spec: 4 source files + 5 data files + tests
- Questions for user: 0 (all resolved in planning)
- Integration points identified: 4
- All file locations verified
- All changes are mechanical string/range replacements
- No questions file needed - spec was complete

---

## Phase 1: Update Source Files

### Task 1.1: Update ConfigManager._get_week_config_filename()
- **File:** `league_helper/util/ConfigManager.py`
- **Lines:** 231-256
- **Change:** Update week range logic from (1-5, 6-11, 12-17) to (1-5, 6-9, 10-13, 14-17)
- **Tests:** `tests/league_helper/util/test_ConfigManager_week_config.py`
- **Status:** [ ] Not started

**Implementation:**
```python
def _get_week_config_filename(self, week: int) -> str:
    if 1 <= week <= 5:
        return "week1-5.json"
    elif 6 <= week <= 9:
        return "week6-9.json"
    elif 10 <= week <= 13:
        return "week10-13.json"
    elif 14 <= week <= 17:
        return "week14-17.json"
    else:
        raise ValueError(f"Invalid week number: {week}. Must be between 1 and 17.")
```

### Task 1.2: Update ConfigGenerator.py
- **File:** `simulation/ConfigGenerator.py`
- **Lines:** 343, 364
- **Change:** Update `required_files` list and loop references
- **Tests:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Changes:**
- Line 343: `required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']`
- Line 364: Update loop to iterate over new filenames

### Task 1.3: Update SimulationManager.py
- **File:** `simulation/SimulationManager.py`
- **Lines:** 578, 878, and all week range references
- **Change:** Update `required_files`, `week_file_mapping`, and week range keys
- **Tests:** `tests/simulation/test_simulation_manager.py`
- **Status:** [ ] Not started

**Changes:**
- Line 578: Update `required_files` list
- Line 878: Update `week_file_mapping` dict:
  ```python
  week_file_mapping = {
      '1-5': 'week1-5.json',
      '6-9': 'week6-9.json',
      '10-13': 'week10-13.json',
      '14-17': 'week14-17.json'
  }
  ```
- All other references to '6-11' → '6-9' and '10-13', '12-17' → '14-17'

### Task 1.4: Update ResultsManager.py
- **File:** `simulation/ResultsManager.py`
- **Lines:** 425-427, 524-526, 589, 609-611, 775
- **Change:** Update all week file mappings
- **Tests:** `tests/simulation/test_ResultsManager.py`
- **Status:** [ ] Not started

**Changes:**
- Lines 425-427: Update week-to-filename mapping
- Lines 524-526: Update week-to-filename mapping
- Line 589: Update `required_files` list
- Lines 609-611: Update filename-to-range mapping
- Line 775: Update `CONFIG_FILES` constant

---

## Phase 2: Create/Update Data Files

### Task 2.1: Create week6-9.json
- **File:** `data/configs/week6-9.json`
- **Source:** Copy from `data/configs/week6-11.json`
- **Status:** [ ] Not started

### Task 2.2: Create week10-13.json
- **File:** `data/configs/week10-13.json`
- **Source:** Copy from `data/configs/week6-11.json`
- **Status:** [ ] Not started

### Task 2.3: Create week14-17.json
- **File:** `data/configs/week14-17.json`
- **Source:** Copy from `data/configs/week12-17.json`
- **Status:** [ ] Not started

### Task 2.4: Delete old config files
- **Files:** `data/configs/week6-11.json`, `data/configs/week12-17.json`
- **Action:** Delete after new files created and tested
- **Status:** [ ] Not started

---

## Phase 3: Update Tests

### Task 3.1: Update test_ConfigManager_week_config.py
- **File:** `tests/league_helper/util/test_ConfigManager_week_config.py`
- **Changes:**
  - Update `create_configs_folder()` to create 4 files instead of 3
  - Update `TestGetWeekConfigFilename` class tests
  - Update boundary tests for new week ranges (9→10, 13→14)
  - Add tests for weeks 9, 10, 13, 14
- **Status:** [ ] Not started

### Task 3.2: Review other test files
- **Files:** 14 other test files with week config references
- **Action:** Search and update any hardcoded week range references
- **Status:** [ ] Not started

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| `_get_week_config_filename()` | ConfigManager.py | `_load_week_config()` | ConfigManager.py:276 | N/A (already calls it) |
| New week mappings | SimulationManager.py | `_save_optimal_configs()` | SimulationManager.py:815 | Task 1.3 |
| New week mappings | ResultsManager.py | `save_optimal_configs_folder()` | ResultsManager.py:460 | Task 1.4 |
| New week mappings | ConfigGenerator.py | `_load_baseline_config()` | ConfigGenerator.py:362 | Task 1.2 |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Week mapping | if 1-5 → week1-5.json | ConfigManager.py:249-250 | `if 1 <= week <= 5` |
| Week mapping | if 6-9 → week6-9.json | ConfigManager.py:251-252 | `elif 6 <= week <= 9` |
| Week mapping | if 10-13 → week10-13.json | ConfigManager.py:253-254 | `elif 10 <= week <= 13` |
| Week mapping | if 14-17 → week14-17.json | ConfigManager.py:255-256 | `elif 14 <= week <= 17` |

---

## Data Flow Traces

### Requirement: Week config loading
```
Entry: run_league_helper.py
  → LeagueHelperManager.__init__()
  → ConfigManager.__init__()
  → _load_config()
  → _load_week_config()
  → _get_week_config_filename()  ← MODIFIED
  → Output: Merged config with week-specific params
```

### Requirement: Simulation config saving
```
Entry: run_simulation.py
  → SimulationManager.run_iterative_optimization()
  → _save_optimal_configs()
  → week_file_mapping lookup  ← MODIFIED
  → Output: 4 week config files saved
```

---

## Edge Cases

| Edge Case | Expected Behavior | Test |
|-----------|-------------------|------|
| Week 5 | Returns week1-5.json | TestGetWeekConfigFilename.test_weeks_1_to_5 |
| Week 6 | Returns week6-9.json | TestGetWeekConfigFilename.test_weeks_6_to_9 |
| Week 9 | Returns week6-9.json | NEW TEST NEEDED |
| Week 10 | Returns week10-13.json | NEW TEST NEEDED |
| Week 13 | Returns week10-13.json | NEW TEST NEEDED |
| Week 14 | Returns week14-17.json | NEW TEST NEEDED |
| Week 17 | Returns week14-17.json | TestGetWeekConfigFilename.test_weeks_14_to_17 |
| Week 0 | Raises ValueError | TestGetWeekConfigFilename.test_week_0_raises_error |
| Week 18 | Raises ValueError | TestGetWeekConfigFilename.test_week_18_raises_error |

---

## Progress Notes

**Last Updated:** 2025-12-13
**Current Status:** Verification complete (24/24), ready for implementation
**Next Steps:** Execute Phase 1 tasks (source file changes)
**Blockers:** None

### Verification Findings
- ConfigManager.py: Lines 249-256 confirmed
- ConfigGenerator.py: Lines 343, 364 confirmed
- SimulationManager.py: Lines 578, 878, 930-933 confirmed
- ResultsManager.py: Lines 424-427, 523-526, 589, 608-611, 775 confirmed
- All changes are mechanical week range string updates
