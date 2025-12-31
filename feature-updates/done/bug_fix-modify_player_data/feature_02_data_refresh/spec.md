# Feature 02: Data Refresh After Modifications - Specification

**Created:** 2025-12-31
**Last Updated:** 2025-12-31 12:30
**Status:** DEEP DIVE (Stage 2 in progress)

---

## Feature Goal

Ensure internal data structures (self.players, FantasyPlayer objects) reflect modifications immediately after players are modified in Modify Player Data mode, and verify that changes persist correctly.

---

## Problem Statement

**User Report:** "doesn't appear to actually update the main files" and internal data may not reflect modifications.

**Current Behavior (from research):**
1. User enters Modify Player Data mode
2. User modifies a player (e.g., marks as drafted)
3. ModifyPlayerDataModeManager modifies in-memory FantasyPlayer object directly
4. Calls `update_players_file()` to persist to JSON
5. User can perform MORE modifications without returning to main menu
6. Eventually user returns to main menu
7. LeagueHelperManager calls `reload_player_data()` before displaying menu

**Uncertainty:**
- Do subsequent queries within the same session see updated values?
- Do changes persist correctly after `reload_player_data()` is called?
- Is there actually a bug, or just missing tests?

---

## Components Affected

### 1. ModifyPlayerDataModeManager

**File:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py

**Menu Loop:** Lines 103-148
- Allows multiple operations without returning to main menu
- **NO reload or refresh called within the loop**

**Modification Methods:**
1. `_mark_player_as_drafted()` (lines 182-240)
   - Line 228: `selected_player.drafted_by = Constants.FANTASY_TEAM_NAME` (direct modification)
   - Line 239: `self.player_manager.update_players_file()` (persist to JSON)

2. `_drop_player()` (lines 241-291)
   - Line 281: `selected_player.drafted_by = ""` (direct modification)
   - Line 285: `self.player_manager.update_players_file()` (persist to JSON)

3. `_lock_player()` (lines 292-386)
   - Toggles `selected_player.locked` (direct modification)
   - Line 383: `self.player_manager.update_players_file()` (persist to JSON)

**Key Observation:** All methods modify the in-memory object BEFORE calling update_players_file().

### 2. PlayerManager

**File:** league_helper/util/PlayerManager.py

**Relevant Methods:**
- `update_players_file()` (lines 451-584)
  - Writes drafted_by and locked fields to JSON files
  - **Depends on Feature 01** to work correctly

- `reload_player_data()` (lines 587-615)
  - Reloads players from JSON files (`load_players_from_json()`)
  - Reloads team roster (`load_team()`)
  - **Question:** Does this replace in-memory list or update it?

### 3. LeagueHelperManager

**File:** league_helper/LeagueHelperManager.py

**Main Menu Loop:** Line 125
- Calls `self.player_manager.reload_player_data()` BEFORE displaying menu
- Ensures data is current when entering any mode

---

## Current Implementation Analysis

**How modifications work:**
```python
# Example: _mark_player_as_drafted() line 228
selected_player.drafted_by = Constants.FANTASY_TEAM_NAME  # Modifies in-memory object
self.player_manager.update_players_file()                 # Persists to JSON
# Returns to menu loop - NO reload called
```

**Python Behavior:**
- `selected_player` is a reference to a FantasyPlayer object in `self.player_manager.players` list
- Python uses pass-by-reference for objects
- Modifying `selected_player.drafted_by` SHOULD modify the actual object in the list

**Expected:** Changes are visible immediately in subsequent queries

**Actual:** UNKNOWN - No tests verify this

---

## Test Coverage Gap

**Current Tests:** `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py`
- ✅ Tests that in-memory object is updated
- ✅ Tests that update_players_file() is called
- ❌ **NOT TESTED:** Subsequent queries see updated value
- ❌ **NOT TESTED:** Multiple modifications in same session work correctly
- ❌ **NOT TESTED:** Changes persist across reload_player_data()
- ❌ **NOT TESTED:** End-to-end integration with real file I/O

**Missing Test Scenarios:**
1. Mark Player A as drafted → Search for Player A → Verify shows as drafted
2. Mark Player A as drafted → Mark Player B as drafted → Verify both show as drafted
3. Mark Player A as drafted → Call reload_player_data() → Verify Player A still drafted
4. Mark Player A as drafted → Exit to main menu → Re-enter mode → Verify Player A still drafted

---

## Dependencies

**This feature depends on:**
- **Feature 01 (File Persistence)** - CRITICAL DEPENDENCY (BLOCKS Feature 02)
  - If update_players_file() doesn't work correctly, changes won't persist to JSON
  - reload_player_data() would reload old data, losing modifications
  - **Decision:** Wait for Feature 01 to complete, then test if data refresh issue persists
  - If issue persists after Feature 01, add tests to verify in-memory behavior
  - Only add explicit refresh mechanism if tests reveal actual bug

**This feature blocks:**
- None (final feature in epic)

**This feature is independent of:**
- All other epic features

---

## Success Criteria

**Feature is successful if:**
1. ✅ Modified player data reflects changes immediately within same session
2. ✅ Subsequent queries see updated values (no stale data)
3. ✅ Changes persist after reload_player_data() is called
4. ✅ Changes persist across exiting and re-entering Modify Player Data mode
5. ✅ All tests pass (100% pass rate)
6. ✅ Integration tests verify end-to-end flow with real files

---

## Research Reference

See `epic/research/FEATURE_02_DATA_REFRESH_DISCOVERY.md` for complete investigation details.

---

**END OF SPEC**
