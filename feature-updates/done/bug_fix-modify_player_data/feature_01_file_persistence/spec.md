# Feature 01: File Persistence Issues - Specification

**Created:** 2025-12-31
**Last Updated:** 2025-12-31 12:00
**Status:** DEEP DIVE (Stage 2 in progress)

---

## Feature Goal

Remove unwanted .bak file creation and ensure player_data/*.json files are properly updated when players are modified in Modify Player Data mode.

---

## Problem Statement

When modifying player data through the Modify Player Data mode, the system creates unwanted .bak backup files. The user explicitly does not want these files, as they clutter the data directory and are not excluded from git version control.

**Current Behavior:**
- Every call to `PlayerManager.update_players_file()` creates 6 .bak files (one per position)
- Files created: qb_data.bak, rb_data.bak, wr_data.bak, te_data.bak, k_data.bak, dst_data.bak
- .bak files are NOT in .gitignore, so they would be tracked by git

**Expected Behavior:**
- No .bak files created during modify operations
- JSON files updated correctly without backup files

---

## Components Affected

### 1. PlayerManager (league_helper/util/PlayerManager.py)

**Method:** `update_players_file()` (lines 451-584)

**Bug Location:** Lines 553-556
```python
# Task 1.7: Create backup file (spec lines 162-165)
backup_path = json_path.with_suffix('.bak')
if json_path.exists():
    import shutil
    shutil.copy2(json_path, backup_path)
```

**Fix Required:** Remove these 4 lines

**Method Flow:**
1. Group players by position (lines 483-493)
2. For each position (QB, RB, WR, TE, K, DST):
   - Read existing JSON file
   - Extract players array from position key
   - Selectively update ONLY drafted_by and locked fields
   - **[BUG] Create .bak backup file (lines 553-556)**
   - Write to .tmp file (atomic write pattern)
   - Atomically replace .json file with .tmp file

**Callers of update_players_file():**
- `ModifyPlayerDataModeManager._mark_player_as_drafted()` (line 239)
- `ModifyPlayerDataModeManager._drop_player()` (line 285)
- `ModifyPlayerDataModeManager._lock_player()` (line 383)
- `AddToRosterModeManager` (also calls this method)

---

## Atomic Write Pattern Verification

**Current Implementation:** (lines 558-566)
```python
# Wrap array back in object with position key
json_data_to_write = {position_key: players_array}
tmp_path = json_path.with_suffix('.tmp')
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(json_data_to_write, f, indent=2)

# Atomic replace (overwrites existing .json file)
tmp_path.replace(json_path)
```

**Analysis:**
- Uses pathlib.Path.replace() which is atomic on POSIX systems
- Writes to .tmp file first, then replaces .json file
- This pattern provides crash safety WITHOUT needing .bak files

**Verification Needed:**
- Confirm tmp_path.replace() works correctly on Windows (this project runs on win32)
- Verify changes persist immediately after method completes
- Ensure changes survive application restart

---

## Files Affected

**Files to Modify:**
1. `league_helper/util/PlayerManager.py`
   - Lines 553-556: Remove .bak file creation code (4 lines)
   - Lines 452-478: Update docstring to remove backup file references
     - Remove "creates backup files (.bak)" from description
     - Remove "Creates .bak backup files" from Side Effects section

**Files to Create:**
2. `tests/league_helper/util/test_PlayerManager_file_updates.py` (NEW)
   - Test update_players_file() method
   - Verify drafted_by persistence
   - Verify locked persistence
   - Verify NO .bak files created
   - Verify atomic write pattern works

**Files to Update:**
3. `.gitignore`
   - Add `*.bak` pattern to prevent accidental commit of backup files (defensive measure)

---

## Test Coverage Gap

**Current State:**
- `tests/league_helper/util/test_PlayerManager_json_loading.py` - Tests JSON loading
- `tests/league_helper/util/test_PlayerManager_scoring.py` - Tests scoring calculations
- **NO tests for update_players_file() method**

**Required Tests:**

**Unit Tests (mocked file system):**
1. Test drafted_by field persistence (mocked)
2. Test locked field persistence (mocked)
3. Verify NO .bak files created after updates (mocked)
4. Test error handling (permission errors, JSON errors) (mocked)

**Integration Tests (real file I/O):**
1. Test atomic write pattern (tmp → replace) with real files on Windows
2. Verify JSON file contents match expected format (real files)
3. Verify changes persist immediately after method completes
4. Verify changes persist across simulated app restarts
5. Verify NO .bak files created in real filesystem

---

## Edge Cases Already Handled

The existing implementation handles:

1. **Permission errors** (lines 575-579)
   - Raises PermissionError with clear message

2. **JSON parse errors** (lines 570-574)
   - Raises json.JSONDecodeError if file corrupted

3. **Missing JSON files** (lines 504-510)
   - Raises FileNotFoundError with helpful message

---

## Dependencies

**This feature depends on:**
- PlayerManager class structure (already exists)
- Position-specific JSON files in data/player_data/ (created by player-data-fetcher)
- FantasyPlayer.drafted_by and .locked fields (already exist)

**This feature blocks:**
- Feature 02 (Data Refresh) - Depends on files being updated correctly

**This feature is independent of:**
- All other epic features (standalone fix)

---

## Success Criteria

**Feature is successful if:**
1. ✅ NO .bak files created during any modify operations
2. ✅ player_data/*.json files updated correctly with drafted_by and locked fields
3. ✅ Changes persist immediately (visible in subsequent reads)
4. ✅ Changes persist across application restarts
5. ✅ All tests pass (100% pass rate)
6. ✅ No regression in existing modify operations

---

## Research Reference

See `epic/research/FEATURE_01_FILE_PERSISTENCE_DISCOVERY.md` for complete investigation details.

---

**END OF SPEC**
