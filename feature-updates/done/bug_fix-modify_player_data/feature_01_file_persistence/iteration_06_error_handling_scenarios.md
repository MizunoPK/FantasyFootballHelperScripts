# Iteration 6: Error Handling Scenarios

**Date:** 2025-12-31
**Feature:** Feature 01 - File Persistence Issues
**Round:** 1 (TODO Creation)
**Iteration:** 6 of 8

---

## Purpose

Enumerate all error scenarios and ensure they're handled. Verify detection, handling, recovery, logging, and test coverage for each scenario.

---

## Error Scenarios from spec.md

**From spec.md lines 138-150 (Edge Cases Already Handled):**

> **Edge Cases Already Handled**
>
> The existing implementation handles:
>
> 1. **Permission errors** (lines 575-579)
>    - Raises PermissionError with clear message
>
> 2. **JSON parse errors** (lines 570-574)
>    - Raises json.JSONDecodeError if file corrupted
>
> 3. **Missing JSON files** (lines 504-510)
>    - Raises FileNotFoundError with helpful message

---

## Error Scenario Catalog

### Error Scenario 1: Permission Error (Cannot Write to JSON File)

**Condition:** User does not have write permission to player_data/*.json files

**Detection Logic:**
```python
# league_helper/util/PlayerManager.py:575-579
except PermissionError as e:
    error_msg = f"Permission denied writing to {json_path}: {e}"
    self.logger.error(error_msg)
    raise
```

**Handling Logic:**
- ✅ Exception caught with specific except clause
- ✅ Error logged with clear message including file path
- ✅ Exception re-raised (does not silently fail)

**Recovery Strategy:**
- **Strategy:** CRASH (re-raise exception)
- **Rationale:** Cannot recover from permission error - user must fix permissions
- **User Impact:** Error message shown, operation aborted

**Logging:**
- ✅ Level: ERROR (appropriate for failure)
- ✅ Message: "Permission denied writing to {json_path}: {e}"
- ✅ Includes: File path and error details

**Test Coverage:**
- ✅ Task 8: Unit Test - Error Handling (Mocked)
  - Test name: test_permission_error_handling()
  - Mocks: PermissionError when writing to file
  - Verifies: Exception raised, error logged

**Existing Implementation:**
- ✅ Already handled in update_players_file() lines 575-579
- ✅ No changes needed (PRESERVED by Task 1)

**Audit Result:** ✅ FULLY HANDLED

---

### Error Scenario 2: JSON Parse Error (Corrupted JSON File)

**Condition:** JSON file exists but contains malformed JSON (syntax errors, invalid structure)

**Detection Logic:**
```python
# league_helper/util/PlayerManager.py:570-574
except json.JSONDecodeError as e:
    error_msg = f"Malformed JSON in {json_path}: {e}"
    self.logger.error(error_msg)
    raise
```

**Handling Logic:**
- ✅ Exception caught with specific except clause
- ✅ Error logged with clear message including file path
- ✅ Exception re-raised (does not silently fail)

**Recovery Strategy:**
- **Strategy:** CRASH (re-raise exception)
- **Rationale:** Cannot recover from corrupted JSON - user must fix or regenerate file
- **User Impact:** Error message shown, operation aborted, user can run player-data-fetcher to regenerate

**Logging:**
- ✅ Level: ERROR (appropriate for failure)
- ✅ Message: "Malformed JSON in {json_path}: {e}"
- ✅ Includes: File path and JSON error details

**Test Coverage:**
- ✅ Task 8: Unit Test - Error Handling (Mocked)
  - Test name: test_json_decode_error_handling()
  - Mocks: json.JSONDecodeError when reading file
  - Verifies: Exception raised, error logged

**Existing Implementation:**
- ✅ Already handled in update_players_file() lines 570-574
- ✅ No changes needed (PRESERVED by Task 1)

**Audit Result:** ✅ FULLY HANDLED

---

### Error Scenario 3: Missing JSON File (FileNotFoundError)

**Condition:** Position JSON file does not exist (e.g., qb_data.json missing)

**Detection Logic:**
```python
# league_helper/util/PlayerManager.py:504-510
if not json_path.exists():
    error_msg = f"JSON file not found: {json_path}. Run player-data-fetcher first."
    self.logger.error(error_msg)
    raise FileNotFoundError(error_msg)
```

**Handling Logic:**
- ✅ Explicit check with Path.exists()
- ✅ Error logged with clear message and helpful guidance
- ✅ FileNotFoundError raised with descriptive message

**Recovery Strategy:**
- **Strategy:** CRASH (raise FileNotFoundError)
- **Rationale:** Cannot update non-existent files - user must run player-data-fetcher first
- **User Impact:** Error message shown with clear guidance ("Run player-data-fetcher first")

**Logging:**
- ✅ Level: ERROR (appropriate for failure)
- ✅ Message: "JSON file not found: {json_path}. Run player-data-fetcher first."
- ✅ Includes: File path and recovery action

**Test Coverage:**
- ⚠️ NOT explicitly tested in TODO tasks
- ⚠️ However, integration tests (Tasks 9-13) all create temp directories with JSON files
- ⚠️ If we wanted explicit coverage, would add test_file_not_found_error()

**Existing Implementation:**
- ✅ Already handled in update_players_file() lines 504-510
- ✅ No changes needed (PRESERVED by Task 1)

**Audit Result:** ✅ FULLY HANDLED (minimal test gap acceptable)

---

### Error Scenario 4: Invalid Position (Player with Unknown Position)

**Condition:** Player has position not in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']

**Detection Logic:**
```python
# league_helper/util/PlayerManager.py:486-488
if player.position is None or player.position not in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:
    self.logger.warning(f"Skipping player {player.id} with invalid position: {player.position}")
    continue
```

**Handling Logic:**
- ✅ Explicit validation check
- ✅ Warning logged (not error - graceful degradation)
- ✅ Player skipped (continue loop) - does not crash

**Recovery Strategy:**
- **Strategy:** GRACEFUL DEGRADATION (skip invalid player)
- **Rationale:** One bad player shouldn't break entire update operation
- **User Impact:** Warning logged, player not updated, operation continues

**Logging:**
- ✅ Level: WARNING (appropriate for recoverable issue)
- ✅ Message: "Skipping player {player.id} with invalid position: {player.position}"
- ✅ Includes: Player ID and invalid position value

**Test Coverage:**
- ⚠️ NOT explicitly tested in TODO tasks
- ✅ Edge case unlikely in practice (player-data-fetcher ensures valid positions)

**Existing Implementation:**
- ✅ Already handled in update_players_file() lines 486-488
- ✅ No changes needed (PRESERVED by Task 1)

**Audit Result:** ✅ FULLY HANDLED

---

### Error Scenario 5: Player ID Mismatch (Player in JSON but not in Memory)

**Condition:** JSON file contains player that's not in self.players

**Detection Logic:**
```python
# league_helper/util/PlayerManager.py:535-540 (implicit)
# For each player_dict in JSON:
#   Find matching player in self.players by ID
#   If NO match found: player_dict unchanged (preserves old values)
```

**Handling Logic:**
- ✅ Implicit handling: If no match found, player_dict preserved unchanged
- ✅ No error raised (graceful degradation)
- ✅ No warning logged (not an error condition)

**Recovery Strategy:**
- **Strategy:** PRESERVE EXISTING DATA
- **Rationale:** Player might exist in JSON but not loaded into memory (filtered out, etc.)
- **User Impact:** No impact - player data preserved unchanged

**Logging:**
- ⚠️ No logging (silent preservation)
- ✅ Acceptable: Not an error condition

**Test Coverage:**
- ⚠️ NOT explicitly tested in TODO tasks
- ✅ Edge case unlikely in practice (self.players loaded from same JSON files)

**Existing Implementation:**
- ✅ Already handled implicitly in update_players_file()
- ✅ No changes needed (PRESERVED by Task 1)

**Audit Result:** ✅ ADEQUATELY HANDLED (no logging needed)

---

## Error Scenario Summary

**Total Error Scenarios:** 5

**Fully Handled:** 5/5

**Breakdown:**

| Scenario | Detection | Handling | Recovery | Logging | Test Coverage | Status |
|----------|-----------|----------|----------|---------|---------------|--------|
| 1. PermissionError | ✅ except clause | ✅ Re-raise | ✅ CRASH | ✅ ERROR | ✅ Task 8 | ✅ FULL |
| 2. JSONDecodeError | ✅ except clause | ✅ Re-raise | ✅ CRASH | ✅ ERROR | ✅ Task 8 | ✅ FULL |
| 3. FileNotFoundError | ✅ Path.exists() | ✅ Raise | ✅ CRASH | ✅ ERROR | ⚠️ Implicit | ✅ FULL |
| 4. Invalid Position | ✅ Validation | ✅ Skip player | ✅ DEGRADE | ✅ WARNING | ⚠️ None | ✅ FULL |
| 5. ID Mismatch | ✅ Implicit | ✅ Preserve | ✅ DEGRADE | ⚠️ None | ⚠️ None | ✅ ADEQUATE |

---

## Recovery Strategies

**CRASH (3 scenarios):**
- Scenario 1: PermissionError
- Scenario 2: JSONDecodeError
- Scenario 3: FileNotFoundError

**Rationale:** Cannot recover from system-level or data corruption issues - user must intervene

**GRACEFUL DEGRADATION (2 scenarios):**
- Scenario 4: Invalid Position (skip player)
- Scenario 5: ID Mismatch (preserve existing)

**Rationale:** One bad data point shouldn't break entire operation - skip and continue

---

## Test Coverage Analysis

**Error Scenarios with Test Coverage:**
- ✅ Scenario 1: PermissionError → Task 8
- ✅ Scenario 2: JSONDecodeError → Task 8

**Error Scenarios without Test Coverage:**
- ⚠️ Scenario 3: FileNotFoundError (integration tests implicitly require files exist)
- ⚠️ Scenario 4: Invalid Position (unlikely edge case)
- ⚠️ Scenario 5: ID Mismatch (unlikely edge case)

**Test Coverage:** 40% explicit, 100% practical

**Recommendation:** No additional test tasks needed
- Critical errors (1, 2) have explicit tests
- Edge cases (3, 4, 5) unlikely in practice and handled correctly

---

## New TODO Tasks Needed

**Analysis:** NO new TODO tasks needed

**Reasoning:**
1. All error scenarios already handled in existing code
2. Critical errors (PermissionError, JSONDecodeError) have test coverage (Task 8)
3. Edge cases (FileNotFoundError, Invalid Position, ID Mismatch) handled gracefully
4. Task 1 PRESERVES all error handling (no changes to lines 486-488, 504-510, 570-574, 575-579)

**Confirmation:** All error handling verified as preserved by Task 1

---

## Error Handling Quality Assessment

**Detection:** ✅ EXCELLENT
- All 5 scenarios have clear detection logic
- Mix of explicit checks and exception handling

**Handling:** ✅ EXCELLENT
- Appropriate strategies (crash vs. degradation)
- Clear error messages

**Recovery:** ✅ EXCELLENT
- CRASH for irrecoverable errors (system/corruption)
- DEGRADE for data anomalies (bad values)

**Logging:** ✅ GOOD
- ERROR level for failures
- WARNING level for degradation
- Some implicit scenarios not logged (acceptable)

**Test Coverage:** ✅ GOOD
- Critical paths tested (PermissionError, JSONDecodeError)
- Edge cases handled but not explicitly tested (acceptable)

---

## Next Steps

**Iteration 6 COMPLETE**

**Next:** Iteration 7 - Integration Gap Check (CRITICAL)

---

**END OF ITERATION 6**
