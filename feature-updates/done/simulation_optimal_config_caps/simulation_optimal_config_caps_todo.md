# Simulation Optimal Config Caps - TODO

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

### Phase 1: Create Utility Function

- [x] **Task 1.1**: Create `cleanup_old_optimal_folders()` function
  - Location: `simulation/config_cleanup.py` (new file)
  - Signature: `cleanup_old_optimal_folders(config_dir: Path, max_folders: int = 5) -> int`
  - Constant: `MAX_OPTIMAL_FOLDERS = 5`

- [x] **Task 1.2**: Implement cleanup logic
  - Glob `optimal_*` folders in config_dir
  - Sort alphabetically (oldest first)
  - While count >= max_folders: delete oldest
  - Return number deleted

- [x] **Task 1.3**: Add error handling
  - Wrap `shutil.rmtree()` in try/except
  - Log warning on failure, continue
  - Use LoggingManager for logging

### Phase 2: Integrate into SimulationManager

- [x] **Task 2.1**: Import cleanup function in `SimulationManager.py`
- [x] **Task 2.2**: Call cleanup before folder creation (line ~773)

### Phase 3: Integrate into ResultsManager

- [x] **Task 3.1**: Import cleanup function in `ResultsManager.py`
- [x] **Task 3.2**: Call cleanup before folder creation (line ~400)

### Phase 4: Testing

- [x] **Task 4.1**: Create `tests/simulation/test_config_cleanup.py`
- [x] **Task 4.2**: Test: No cleanup when under limit
- [x] **Task 4.3**: Test: Deletes oldest when at limit
- [x] **Task 4.4**: Test: Handles deletion errors gracefully
- [x] **Task 4.5**: Test: Only matches `optimal_*` pattern
- [x] **Task 4.6**: Run full test suite (2174/2174 = 100% pass)

---

## Algorithm Traceability Matrix

| Spec Requirement | Code Location | Status |
|------------------|---------------|--------|
| R1: Folder limit enforcement | `cleanup_old_optimal_folders()` | Pending |
| R2: Oldest by name sort | `sorted(folders)[0]` | Pending |
| R3: Configurable limit (default 5) | `MAX_OPTIMAL_FOLDERS = 5` | Pending |
| R4: Pattern `optimal_*` only | `glob("optimal_*")` | Pending |
| Q5: Error handling | `try/except` with warning | Pending |

---

## Integration Matrix

| New Code | Caller | Call Site | Status |
|----------|--------|-----------|--------|
| `cleanup_old_optimal_folders()` | SimulationManager | Line ~772 | Pending |
| `cleanup_old_optimal_folders()` | ResultsManager | Line ~400 | Pending |

---

## Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `simulation/config_cleanup.py` | NEW | Cleanup utility function |
| `simulation/SimulationManager.py` | MODIFY | Add import + call cleanup |
| `simulation/ResultsManager.py` | MODIFY | Add import + call cleanup |
| `tests/simulation/test_config_cleanup.py` | NEW | Unit tests |

---

## Progress Notes

**Last Updated:** 2025-12-06
**Current Status:** Step 1 - TODO created
**Next Steps:** Execute verification iterations
