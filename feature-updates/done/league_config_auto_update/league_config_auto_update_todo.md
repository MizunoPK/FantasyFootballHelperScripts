# League Config Auto Update - TODO

## Iteration Progress Tracker

**First Round (7 iterations):**
- [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7

**Second Round (9 iterations):**
- [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16

**Third Round (8 iterations):**
- [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24

**Notes:** All questions resolved during planning phase. No questions file needed.

---

## Implementation Tasks

### Phase 1: Update ResultsManager - Add INJURY_PENALTIES to PRESERVE_KEYS

- [x] **Task 1.1**: Add INJURY_PENALTIES to PRESERVE_KEYS list in `update_league_config()` (line ~681)

### Phase 2: Create update_configs_folder() Method

- [x] **Task 2.1**: Add new `update_configs_folder()` method to ResultsManager
  - Signature: `update_configs_folder(optimal_folder: Path, target_folder: Path) -> None`
  - Handles all 4 config files

- [x] **Task 2.2**: Implement league_config.json update logic
  - Load optimal and original files
  - Preserve: CURRENT_NFL_WEEK, NFL_SEASON, MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS, INJURY_PENALTIES
  - Keep performance_metrics
  - If original doesn't exist, copy optimal directly

- [x] **Task 2.3**: Implement week file update logic
  - For each week file (week1-5.json, week6-11.json, week12-17.json)
  - Apply MATCHUP → SCHEDULE mapping
  - Log warning if MATCHUP_SCORING missing
  - Keep performance_metrics
  - If original doesn't exist, copy optimal directly

### Phase 3: Update SimulationManager

- [x] **Task 3.1**: Replace shutil.copy2 loop (lines ~841-845) with call to `update_configs_folder()`

### Phase 4: Testing

- [x] **Task 4.1**: Add tests for `update_configs_folder()` method
- [x] **Task 4.2**: Test: Preserves league_config.json parameters
- [x] **Task 4.3**: Test: Applies MATCHUP → SCHEDULE mapping
- [x] **Task 4.4**: Test: Handles missing target files (first run)
- [x] **Task 4.5**: Test: Logs warning for missing MATCHUP_SCORING
- [x] **Task 4.6**: Test: Keeps performance_metrics
- [x] **Task 4.7**: Run full test suite (100% pass required) - **2184 tests passed**

---

## Algorithm Traceability Matrix

| Spec Requirement | Code Location | Status |
|------------------|---------------|--------|
| R1: Preserve params in league_config | `ResultsManager.py:765-772` | ✓ Complete |
| R2: MATCHUP → SCHEDULE mapping | `ResultsManager.py:826-853` | ✓ Complete |
| R3: Replace shutil.copy2 | `SimulationManager.py:840-841` | ✓ Complete |
| R4: Update all other params | `ResultsManager.py:799-806` | ✓ Complete |
| Q4: Keep performance_metrics | Config copied unchanged | ✓ Complete |
| Q6: Add INJURY_PENALTIES | `ResultsManager.py:681, 771` | ✓ Complete |

---

## Integration Matrix

| New Code | Caller | Call Site | Status |
|----------|--------|-----------|--------|
| `update_configs_folder()` | SimulationManager | Line ~841 | ✓ Complete |

---

## Files Modified

| File | Change Type | Description |
|------|-------------|-------------|
| `simulation/ResultsManager.py` | MODIFIED | Added INJURY_PENALTIES to PRESERVE_KEYS (line ~681), added `update_configs_folder()` (lines 737-824), added `_apply_matchup_to_schedule_mapping()` (lines 826-853) |
| `simulation/SimulationManager.py` | MODIFIED | Replaced shutil.copy2 loop with call to `update_configs_folder()` (line ~841) |
| `tests/simulation/test_ResultsManager.py` | MODIFIED | Added `TestUpdateConfigsFolder` class (8 tests), `TestApplyMatchupToScheduleMapping` class (3 tests) |

---

## Progress Notes

**Last Updated:** 2025-12-06
**Current Status:** Implementation Complete - QC in progress
**Tests:** 2184 tests passed (100%)
