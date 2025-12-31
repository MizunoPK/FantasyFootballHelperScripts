# Iteration 4: Algorithm Traceability Matrix

**Date:** 2025-12-31
**Feature:** Feature 01 - File Persistence Issues
**Round:** 1 (TODO Creation)
**Iteration:** 4 of 8

---

## Purpose

Map EVERY algorithm in spec.md to exact implementation location and TODO task. This prevents "implemented wrong algorithm" bugs.

---

## Algorithms Extracted from spec.md

### Category 1: Main Algorithm (update_players_file Method Flow)

**From spec.md lines 46-55:**

> **Method Flow:**
> 1. Group players by position (lines 483-493)
> 2. For each position (QB, RB, WR, TE, K, DST):
>    - Read existing JSON file
>    - Extract players array from position key
>    - Selectively update ONLY drafted_by and locked fields
>    - **[BUG] Create .bak backup file (lines 553-556)**
>    - Write to .tmp file (atomic write pattern)
>    - Atomically replace .json file with .tmp file

### Category 2: Edge Case Handling

**From spec.md lines 138-150:**

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

### Category 3: Test Verification Algorithms

**From spec.md lines 122-135:**

> **Unit Tests (mocked file system):**
> 1. Test drafted_by field persistence (mocked)
> 2. Test locked field persistence (mocked)
> 3. Verify NO .bak files created after updates (mocked)
> 4. Test error handling (permission errors, JSON errors) (mocked)
>
> **Integration Tests (real file I/O):**
> 1. Test atomic write pattern (tmp → replace) with real files on Windows
> 2. Verify JSON file contents match expected format (real files)
> 3. Verify changes persist immediately after method completes
> 4. Verify changes persist across simulated app restarts
> 5. Verify NO .bak files created in real filesystem

---

## Algorithm Traceability Matrix

| Algorithm (from spec.md) | Spec Section | Implementation Location | TODO Task | Verified |
|--------------------------|--------------|------------------------|-----------|----------|
| **1. Group players by position** | Method Flow, step 1 (line 47) | PlayerManager.update_players_file() lines 483-493 | Task 1 (preserves this) | ✅ |
| **2. Read existing JSON file** | Method Flow, step 2 (line 49) | PlayerManager.update_players_file() lines 500-520 | Task 1 (preserves this) | ✅ |
| **3. Extract players array from position key** | Method Flow, step 2 (line 50) | PlayerManager.update_players_file() lines 520-530 | Task 1 (preserves this) | ✅ |
| **4. Selectively update drafted_by and locked fields** | Method Flow, step 2 (line 51) | PlayerManager.update_players_file() lines 530-551 | Task 1 (preserves this) | ✅ |
| **5. Create .bak backup file** | Method Flow, step 2 (line 52) - **BUG** | PlayerManager.update_players_file() lines 553-556 | Task 1 (**REMOVES** this) | ✅ |
| **6. Write to .tmp file (atomic write)** | Method Flow, step 2 (line 53) | PlayerManager.update_players_file() lines 558-563 | Task 1 (preserves this) | ✅ |
| **7. Atomically replace .json with .tmp** | Method Flow, step 2 (line 54) | PlayerManager.update_players_file() line 566 | Task 1 (preserves this) | ✅ |
| **8. Handle PermissionError** | Edge Cases, case 1 (lines 142-143) | PlayerManager.update_players_file() lines 575-579 | Task 1 (preserves this) | ✅ |
| **9. Handle JSONDecodeError** | Edge Cases, case 2 (lines 145-146) | PlayerManager.update_players_file() lines 570-574 | Task 1 (preserves this) | ✅ |
| **10. Handle FileNotFoundError** | Edge Cases, case 3 (lines 148-149) | PlayerManager.update_players_file() lines 504-510 | Task 1 (preserves this) | ✅ |
| **11. Update docstring (remove .bak references)** | Files Affected (lines 95-97) | PlayerManager.update_players_file() docstring lines 452-478 | Task 2 | ✅ |
| **12. Add *.bak to .gitignore** | Files Affected (lines 108-110) | .gitignore file (append pattern) | Task 3 | ✅ |
| **13. Test drafted_by persistence (mocked)** | Unit Tests (line 124) | test_PlayerManager_file_updates.py (new test) | Task 5 | ✅ |
| **14. Test locked persistence (mocked)** | Unit Tests (line 125) | test_PlayerManager_file_updates.py (new test) | Task 6 | ✅ |
| **15. Verify NO .bak files created (mocked)** | Unit Tests (line 126) | test_PlayerManager_file_updates.py (new test) | Task 7 | ✅ |
| **16. Test error handling (mocked)** | Unit Tests (line 127) | test_PlayerManager_file_updates.py (new test) | Task 8 | ✅ |
| **17. Test atomic write pattern on Windows** | Integration Tests (line 130) | test_PlayerManager_file_updates.py (new test) | Task 9 | ✅ |
| **18. Verify JSON format matches expected** | Integration Tests (line 131) | test_PlayerManager_file_updates.py (new test) | Task 10 | ✅ |
| **19. Verify changes persist immediately** | Integration Tests (line 132) | test_PlayerManager_file_updates.py (new test) | Task 11 | ✅ |
| **20. Verify changes persist across restarts** | Integration Tests (line 133) | test_PlayerManager_file_updates.py (new test) | Task 12 | ✅ |
| **21. Verify NO .bak files in real filesystem** | Integration Tests (line 134) | test_PlayerManager_file_updates.py (new test) | Task 13 | ✅ |

---

## Detailed Algorithm Mappings

### Algorithm 1-4, 6-10: Preserve Existing Logic (Task 1 context)

**Algorithm from spec.md (Method Flow, lines 47-54):**

> "1. Group players by position (lines 483-493)
> 2. For each position (QB, RB, WR, TE, K, DST):
>    - Read existing JSON file
>    - Extract players array from position key
>    - Selectively update ONLY drafted_by and locked fields
>    - Write to .tmp file (atomic write pattern)
>    - Atomically replace .json file with .tmp file"

**Implementation:**
- Method: PlayerManager.update_players_file()
- File: league_helper/util/PlayerManager.py
- Lines: 451-584
- **Action:** PRESERVE all this logic (do NOT modify)
- **Exception:** Remove lines 553-556 (algorithm #5 - .bak creation)

**Traceability:**
- Algorithms #1, #2, #3, #4, #6, #7 → Task 1 (remove .bak code ONLY)
- Algorithms #8, #9, #10 (error handling) → Task 1 (preserve error handling)

---

### Algorithm 5: Remove .bak Backup File Creation (Task 1)

**Algorithm from spec.md (Method Flow, line 52 - BUG):**

> "**[BUG] Create .bak backup file (lines 553-556)**"

**Current Implementation (TO BE REMOVED):**
```python
# league_helper/util/PlayerManager.py:553-556
backup_path = json_path.with_suffix('.bak')
if json_path.exists():
    import shutil
    shutil.copy2(json_path, backup_path)
```

**Action:** DELETE these 4 lines

**TODO Task Reference:**
- Task 1: Remove .bak File Creation Code
- Spec Reference: spec.md lines 93-98
- File: league_helper/util/PlayerManager.py
- Lines: 553-556

**Acceptance Criteria (from todo.md Task 1):**
- [ ] Lines 553-556 removed from PlayerManager.py
- [ ] Code still compiles without errors
- [ ] No .bak files created when update_players_file() is called

**Traceability:** Algorithm #5 in spec.md → Task 1 → DELETE lines 553-556

---

### Algorithm 11: Update Docstring (Task 2)

**Algorithm from spec.md (Files Affected, lines 95-97):**

> "Lines 452-478: Update docstring to remove backup file references
>  - Remove 'creates backup files (.bak)' from description
>  - Remove 'Creates .bak backup files' from Side Effects section"

**Implementation:**
- Method: PlayerManager.update_players_file()
- File: league_helper/util/PlayerManager.py
- Lines: 452-478 (docstring)

**Changes:**
1. Line 460: Remove "and creates backup files (.bak) before updating for manual recovery if needed"
2. Line 468: Remove "- Creates .bak backup files"

**TODO Task Reference:**
- Task 2: Update Method Docstring
- Spec Reference: spec.md lines 96-98

**Acceptance Criteria (from todo.md Task 2):**
- [ ] Docstring no longer mentions .bak files
- [ ] Docstring accurately describes current behavior (atomic write only)
- [ ] Side Effects section updated

**Traceability:** Algorithm #11 in spec.md → Task 2 → UPDATE docstring lines 460, 468

---

### Algorithm 12: Add *.bak to .gitignore (Task 3)

**Algorithm from spec.md (Files Affected, lines 108-110):**

> "3. `.gitignore`
>    - Add `*.bak` pattern to prevent accidental commit of backup files (defensive measure)"

**Implementation:**
- File: .gitignore (root of repository)
- Action: Append pattern `*.bak` on new line

**TODO Task Reference:**
- Task 3: Add *.bak to .gitignore
- Spec Reference: spec.md lines 108-110

**Acceptance Criteria (from todo.md Task 3):**
- [ ] `*.bak` added to .gitignore file
- [ ] Defensive measure prevents future .bak file commits

**Traceability:** Algorithm #12 in spec.md → Task 3 → APPEND to .gitignore

---

### Algorithms 13-16: Unit Tests (Mocked) (Tasks 5-8)

**Algorithms from spec.md (Unit Tests, lines 123-127):**

> "**Unit Tests (mocked file system):**
> 1. Test drafted_by field persistence (mocked)
> 2. Test locked field persistence (mocked)
> 3. Verify NO .bak files created after updates (mocked)
> 4. Test error handling (permission errors, JSON errors) (mocked)"

**Implementation:**
- File: tests/league_helper/util/test_PlayerManager_file_updates.py (NEW)
- Tests use unittest.mock to mock file system operations
- Tests verify JSON data written (without actual file I/O)

**TODO Task References:**
- Algorithm #13 → Task 5: Unit Test - drafted_by Persistence (Mocked)
- Algorithm #14 → Task 6: Unit Test - locked Persistence (Mocked)
- Algorithm #15 → Task 7: Unit Test - NO .bak Files Created (Mocked)
- Algorithm #16 → Task 8: Unit Test - Error Handling (Mocked)

**Acceptance Criteria (from todo.md Tasks 5-8):**
- Each test uses mocked file system (no real I/O)
- Each test verifies specific behavior in isolation
- All tests pass with 100% pass rate

**Traceability:**
- Algorithm #13 in spec.md → Task 5 → test_drafted_by_persistence_mocked()
- Algorithm #14 in spec.md → Task 6 → test_locked_persistence_mocked()
- Algorithm #15 in spec.md → Task 7 → test_no_bak_files_mocked()
- Algorithm #16 in spec.md → Task 8 → test_error_handling_mocked()

---

### Algorithms 17-21: Integration Tests (Real I/O) (Tasks 9-13)

**Algorithms from spec.md (Integration Tests, lines 130-134):**

> "**Integration Tests (real file I/O):**
> 1. Test atomic write pattern (tmp → replace) with real files on Windows
> 2. Verify JSON file contents match expected format (real files)
> 3. Verify changes persist immediately after method completes
> 4. Verify changes persist across simulated app restarts
> 5. Verify NO .bak files created in real filesystem"

**Implementation:**
- File: tests/league_helper/util/test_PlayerManager_file_updates.py (NEW)
- Tests use real file I/O with tmp_path fixture
- Tests verify actual files on disk (Windows platform)

**TODO Task References:**
- Algorithm #17 → Task 9: Integration Test - Atomic Write Pattern on Windows
- Algorithm #18 → Task 10: Integration Test - JSON File Contents Match Expected Format
- Algorithm #19 → Task 11: Integration Test - Changes Persist Immediately
- Algorithm #20 → Task 12: Integration Test - Changes Persist Across Restarts
- Algorithm #21 → Task 13: Integration Test - NO .bak Files Created in Real Filesystem

**Acceptance Criteria (from todo.md Tasks 9-13):**
- Each test uses real file I/O (tmp_path fixture)
- Tests verify actual filesystem state
- Windows-specific verification (Path.replace() behavior)
- All tests pass with 100% pass rate

**Traceability:**
- Algorithm #17 in spec.md → Task 9 → test_atomic_write_pattern_windows()
- Algorithm #18 in spec.md → Task 10 → test_json_format_verification()
- Algorithm #19 in spec.md → Task 11 → test_changes_persist_immediately()
- Algorithm #20 in spec.md → Task 12 → test_changes_persist_across_restarts()
- Algorithm #21 in spec.md → Task 13 → test_no_bak_files_real_filesystem()

---

## Matrix Verification

**Count algorithms in spec.md:** 21

**Count rows in matrix:** 21

**✅ ALL ALGORITHMS TRACED**

---

## Coverage Summary

**Code Modifications (3 algorithms):**
- ✅ Algorithm #5: Remove .bak creation (Task 1)
- ✅ Algorithm #11: Update docstring (Task 2)
- ✅ Algorithm #12: Add to .gitignore (Task 3)

**Preserved Logic (9 algorithms):**
- ✅ Algorithms #1-4, #6-10: Existing update_players_file() logic (preserved)

**Unit Tests (4 algorithms):**
- ✅ Algorithms #13-16: Mocked unit tests (Tasks 5-8)

**Integration Tests (5 algorithms):**
- ✅ Algorithms #17-21: Real I/O integration tests (Tasks 9-13)

**Total:** 21 algorithms mapped to 13 TODO tasks

---

## Critical Findings

**Algorithm #5 (Remove .bak creation):**
- This is the ONLY code removal
- All other logic PRESERVED
- Atomic write pattern (algorithms #6-7) remains intact

**Algorithm #17 (Atomic write on Windows):**
- CRITICAL: Must verify Path.replace() works on win32
- Test platform: MINGW64_NT-10.0-19045 (from env context)
- Atomic behavior NOT guaranteed on Windows

**Algorithms #15 and #21 (NO .bak verification):**
- Two separate verifications (mocked and real filesystem)
- Both must pass to confirm fix is complete

---

## Next Steps

**Iteration 4 COMPLETE**

**Next:** Iteration 4a - TODO Specification Audit (MANDATORY GATE)

---

**END OF ITERATION 4**
