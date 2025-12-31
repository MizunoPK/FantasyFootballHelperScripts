# Feature 01: File Persistence Issues - TODO

**Created:** 2025-12-31
**Status:** ROUND 1 IN PROGRESS

---

## TODO Tasks

### CODE CHANGES

#### Task 1: Remove .bak File Creation Code
**Spec Reference:** spec.md lines 93-98
**File:** `league_helper/util/PlayerManager.py`
**Lines:** 553-556
**Action:** Remove the 4 lines that create .bak backup files

```python
# REMOVE THESE 4 LINES:
backup_path = json_path.with_suffix('.bak')
if json_path.exists():
    import shutil
    shutil.copy2(json_path, backup_path)
```

**Acceptance Criteria:**
- [ ] Lines 553-556 removed from PlayerManager.py
- [ ] Code still compiles without errors
- [ ] No .bak files created when update_players_file() is called

---

#### Task 2: Update Method Docstring
**Spec Reference:** spec.md lines 96-98
**File:** `league_helper/util/PlayerManager.py`
**Lines:** 452-478
**Action:** Update update_players_file() docstring to remove backup file references

**Changes needed:**
1. Remove "and creates backup files (.bak) before updating for manual recovery if needed" from description (line 460)
2. Remove "- Creates .bak backup files" from Side Effects section (line 468)

**Acceptance Criteria:**
- [ ] Docstring no longer mentions .bak files
- [ ] Docstring accurately describes current behavior (atomic write only)
- [ ] Side Effects section updated

---

#### Task 3: Add *.bak to .gitignore
**Spec Reference:** spec.md lines 108-110
**File:** `.gitignore`
**Action:** Add `*.bak` pattern to prevent accidental commit of backup files

**Acceptance Criteria:**
- [ ] `*.bak` added to .gitignore file
- [ ] Defensive measure prevents future .bak file commits

---

### TEST FILE CREATION

#### Task 4: Create Test File for update_players_file()
**Spec Reference:** spec.md lines 100-106
**File:** `tests/league_helper/util/test_PlayerManager_file_updates.py` (NEW)
**Action:** Create new test file with comprehensive test coverage

**Test file structure:**
- Import statements
- Fixtures (sample players, mock PlayerManager, temp directories)
- Unit test classes (mocked file system)
- Integration test classes (real file I/O)

**Acceptance Criteria:**
- [ ] New test file created in correct location
- [ ] File imports all necessary modules
- [ ] Fixtures defined for test data

---

### UNIT TESTS (Mocked File System)

#### Task 5: Unit Test - drafted_by Persistence (Mocked)
**Spec Reference:** spec.md line 124
**Test:** Verify drafted_by field is correctly written to JSON (mocked filesystem)

**Test scenario:**
1. Create mock PlayerManager with sample players
2. Modify player.drafted_by field
3. Call update_players_file() with mocked file operations
4. Verify JSON data written contains correct drafted_by value

**Acceptance Criteria:**
- [ ] Test passes with mocked file system
- [ ] Verifies drafted_by field in JSON data
- [ ] Test is isolated (no real file I/O)

---

#### Task 6: Unit Test - locked Persistence (Mocked)
**Spec Reference:** spec.md line 125
**Test:** Verify locked field is correctly written to JSON (mocked filesystem)

**Test scenario:**
1. Create mock PlayerManager with sample players
2. Modify player.locked field
3. Call update_players_file() with mocked file operations
4. Verify JSON data written contains correct locked value

**Acceptance Criteria:**
- [ ] Test passes with mocked file system
- [ ] Verifies locked field in JSON data
- [ ] Test is isolated (no real file I/O)

---

#### Task 7: Unit Test - NO .bak Files Created (Mocked)
**Spec Reference:** spec.md line 126
**Test:** Verify NO .bak files are created after update_players_file() (mocked filesystem)

**Test scenario:**
1. Create mock PlayerManager
2. Call update_players_file() with mocked file operations
3. Verify shutil.copy2() is NOT called for .bak files
4. Verify no file operations target .bak paths

**Acceptance Criteria:**
- [ ] Test passes with mocked file system
- [ ] Verifies .bak file creation code NOT executed
- [ ] Test is isolated (no real file I/O)

---

#### Task 8: Unit Test - Error Handling (Mocked)
**Spec Reference:** spec.md line 127
**Test:** Verify error handling for permission errors and JSON errors (mocked filesystem)

**Test scenarios:**
1. PermissionError when writing to JSON file
2. json.JSONDecodeError when reading malformed JSON file

**Acceptance Criteria:**
- [ ] Test for PermissionError passes
- [ ] Test for JSONDecodeError passes
- [ ] Errors are handled gracefully with clear messages

---

### INTEGRATION TESTS (Real File I/O)

#### Task 9: Integration Test - Atomic Write Pattern on Windows
**Spec Reference:** spec.md line 130
**Test:** Test atomic write pattern (tmp → replace) with real files on Windows

**Test scenario:**
1. Create temp directory with real JSON files
2. Modify player data
3. Call update_players_file() with real file I/O
4. Verify .tmp file created during write
5. Verify .tmp file replaced .json file atomically
6. Verify Path.replace() works correctly on win32

**Acceptance Criteria:**
- [ ] Test passes with real file I/O on Windows
- [ ] Atomic write pattern verified
- [ ] No .tmp files left behind after completion

---

#### Task 10: Integration Test - JSON File Contents Match Expected Format
**Spec Reference:** spec.md line 131
**Test:** Verify JSON file contents match expected format (real files)

**Test scenario:**
1. Create temp directory with real JSON files
2. Modify player data (drafted_by and locked fields)
3. Call update_players_file()
4. Read JSON file back from disk
5. Verify format matches position_key: [{players}] structure
6. Verify drafted_by and locked fields have correct values

**Acceptance Criteria:**
- [ ] Test passes with real file I/O
- [ ] JSON format verified
- [ ] Field values correct

---

#### Task 11: Integration Test - Changes Persist Immediately
**Spec Reference:** spec.md line 132
**Test:** Verify changes persist immediately after method completes

**Test scenario:**
1. Create temp directory with real JSON files
2. Modify player data
3. Call update_players_file()
4. Immediately read JSON file from disk (same process)
5. Verify changes are visible

**Acceptance Criteria:**
- [ ] Test passes with real file I/O
- [ ] Changes visible immediately after method completes
- [ ] No caching or buffering issues

---

#### Task 12: Integration Test - Changes Persist Across Restarts
**Spec Reference:** spec.md line 133
**Test:** Verify changes persist across simulated app restarts

**Test scenario:**
1. Create temp directory with real JSON files
2. Modify player data
3. Call update_players_file()
4. Simulate restart by creating NEW PlayerManager instance
5. Load data from same JSON files
6. Verify changes persisted

**Acceptance Criteria:**
- [ ] Test passes with real file I/O
- [ ] Changes survive simulated restart
- [ ] Data reloads correctly

---

#### Task 13: Integration Test - NO .bak Files Created in Real Filesystem
**Spec Reference:** spec.md line 134
**Test:** Verify NO .bak files created in real filesystem

**Test scenario:**
1. Create temp directory with real JSON files
2. Call update_players_file() with real file I/O
3. List all files in temp directory
4. Verify NO .bak files exist

**Acceptance Criteria:**
- [ ] Test passes with real file I/O
- [ ] No .bak files found in filesystem
- [ ] Only .json files exist (no .bak, no .tmp)

---

## Task Summary

**Total Tasks:** 13

**Code Changes:** 3 tasks (Tasks 1-3)
- Remove .bak creation code
- Update docstring
- Add to .gitignore

**Test File Creation:** 1 task (Task 4)
- Create new test file

**Unit Tests:** 4 tasks (Tasks 5-8)
- drafted_by persistence (mocked)
- locked persistence (mocked)
- NO .bak files (mocked)
- Error handling (mocked)

**Integration Tests:** 5 tasks (Tasks 9-13)
- Atomic write pattern on Windows
- JSON format verification
- Immediate persistence
- Persistence across restarts
- NO .bak files in real filesystem

---

**Requirements Coverage:** ALL requirements from spec.md mapped to TODO tasks (100% coverage)

**Next:** Iteration 2 - Component Dependency Mapping

---

**END OF TODO**
