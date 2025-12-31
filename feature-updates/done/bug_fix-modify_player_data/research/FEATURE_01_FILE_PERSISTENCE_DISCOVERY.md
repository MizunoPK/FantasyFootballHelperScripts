# Feature 01: File Persistence Issues - Discovery Findings

**Research Date:** 2025-12-31
**Researcher:** Agent
**Feature:** feature_01_file_persistence

---

## Components Identified

**Primary Bug Location:**
- `PlayerManager.update_players_file()` (league_helper/util/PlayerManager.py:451-584)
  - **Lines 553-556: Creates unwanted .bak backup files**
  - Lines 558-566: Atomic write pattern (write to .tmp, then replace .json)

**Callers of update_players_file():**
- `ModifyPlayerDataModeManager._mark_player_as_drafted()` (line 239)
- `ModifyPlayerDataModeManager._drop_player()` (line 285)
- `ModifyPlayerDataModeManager._lock_player()` (line 383)
- `AddToRosterModeManager` (also calls update_players_file)

---

## Method Flow Analysis

**PlayerManager.update_players_file() flow:**

1. **Group players by position** (lines 483-493)
   - Creates Dict[str, List[FantasyPlayer]] keyed by position (QB, RB, WR, TE, K, DST)

2. **For each position** (QB, RB, WR, TE, K, DST):
   - Read existing JSON file (lines 514-515)
   - Extract players array from position key (e.g., "qb_data")
   - Create ID → FantasyPlayer lookup for this position (lines 522-523)
   - **Selectively update ONLY drafted_by and locked fields** (lines 526-548)
   - **🐛 BUG: Create .bak backup file (lines 553-556)**
   - Write to .tmp file with atomic write pattern (lines 561-563)
   - Atomically replace .json file with .tmp file (line 566)

3. **Return success message** (lines 582-584)

---

## Bug Details

### Bug 1: Unwanted .bak File Creation

**Location:** PlayerManager.py lines 553-556
```python
# Task 1.7: Create backup file (spec lines 162-165)
backup_path = json_path.with_suffix('.bak')
if json_path.exists():
    import shutil
    shutil.copy2(json_path, backup_path)
```

**Issue:** Creates backup files (.bak) for all 6 position files:
- data/player_data/qb_data.bak
- data/player_data/rb_data.bak
- data/player_data/wr_data.bak
- data/player_data/te_data.bak
- data/player_data/k_data.bak
- data/player_data/dst_data.bak

**Impact:**
- **.bak files are NOT in .gitignore** (verified C:\Users\kmgam\code\FantasyFootballHelperScripts\.gitignore)
- Files would be tracked by git
- Clutters data directory
- User explicitly does not want these files

**Root Cause:**
- Legacy code from CSV-based system (when manual recovery was needed)
- Atomic write pattern (lines 558-566) already provides safety
- Backup files are redundant

---

### Bug 2: JSON Update Persistence (Verification Needed)

**Location:** PlayerManager.py lines 558-566 (atomic write pattern)

**Current Implementation:**
```python
# Task 1.6: Atomic write pattern (spec lines 162-165)
# Wrap array back in object with position key
json_data_to_write = {position_key: players_array}
tmp_path = json_path.with_suffix('.tmp')
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(json_data_to_write, f, indent=2)

# Atomic replace (overwrites existing .json file)
tmp_path.replace(json_path)
```

**Status:** Appears correct, but need to verify:
1. Does tmp_path.replace() actually overwrite the .json file?
2. Are changes visible immediately after method completes?
3. Do changes persist across app restarts?

**Testing Strategy:**
- Create test that modifies player, calls update_players_file()
- Read JSON file back and verify changes persisted
- Restart app and verify changes still present

---

## Existing Test Coverage

**Test files found:**
- `tests/league_helper/util/test_PlayerManager_json_loading.py` - Tests JSON loading
- `tests/league_helper/util/test_PlayerManager_scoring.py` - Tests scoring calculations

**Gap identified:**
- **No existing tests for update_players_file() method**
- Need to add comprehensive tests for file persistence

---

## Files Affected by Fix

**Files to Modify:**
1. `league_helper/util/PlayerManager.py` (lines 553-556)
   - **Action:** Remove .bak file creation code

**Files to Create:**
2. `tests/league_helper/util/test_PlayerManager_file_updates.py` (NEW)
   - **Action:** Add comprehensive tests for update_players_file()
   - Test atomic write pattern
   - Test drafted_by field persistence
   - Test locked field persistence
   - Verify NO .bak files created

**Files to Update:**
3. `.gitignore` (optional)
   - **Action:** Add *.bak to gitignore (defensive, in case backup files exist)
   - Prevents accidental commit of any .bak files

---

## Edge Cases Identified

1. **Permission errors** (already handled at lines 575-579)
   - If cannot write to .json or .tmp files
   - Raises PermissionError with clear message

2. **JSON parse errors** (already handled at lines 570-574)
   - If existing .json file is malformed
   - Raises json.JSONDecodeError

3. **Missing JSON files** (already handled at lines 504-510)
   - If position JSON file doesn't exist
   - Raises FileNotFoundError with helpful message

4. **Concurrent writes** (NOT handled - potential issue?)
   - What if two processes call update_players_file() simultaneously?
   - Atomic write pattern helps but may not fully protect

---

## Similar Patterns in Codebase

**Other usages of update_players_file():**
- `AddToRosterModeManager` - Uses same method to persist draft choices
- Both modify player.drafted_by and player.locked fields
- Both expect immediate persistence

**Pattern:** Modify in-memory player data → Call update_players_file() → Expect changes persisted

---

## Dependencies

**This feature depends on:**
- PlayerManager class structure (already exists)
- Position-specific JSON files in data/player_data/ (created by player-data-fetcher)
- FantasyPlayer.drafted_by and .locked fields (already exist)

**This feature blocks:**
- Feature 02 (Data Refresh) - Depends on files being updated correctly

---

## Questions for User (Will go in checklist.md)

1. Should we add *.bak to .gitignore as defensive measure?
2. Should we add tests for concurrent write scenarios?
3. Should we clean up existing .bak files in data/player_data/?

---

**Next Steps:**
- Phase 2: Update spec.md with detailed requirements
- Phase 2: Create checklist.md with open questions
- Phase 3: Ask user questions ONE AT A TIME

---

**END OF DISCOVERY DOCUMENT**
