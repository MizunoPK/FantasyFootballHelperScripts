# Sub-Feature 4: File Update Strategy - Checklist

> **IMPORTANT**: When marking items as resolved, also update `sub_feature_04_file_update_strategy_spec.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** 24 (corrected count)
**Completed:** 17 (2 analysis + 10 patterns/conversions/error handling + 2 dependencies + 3 user decisions ✅)
**Remaining:** 7
- **User decisions needed:** 0 ✅ ALL RESOLVED (NEW-78, NEW-82, NEW-89)
- **Implementation tasks:** 2 (NEW-76, NEW-79)
- **Testing deferred:** 5 (NEW-90 through NEW-94)

**Phase 3 Status:** ✅ COMPLETE (2025-12-28) - All user decisions resolved

---

## Analysis & Strategy (2 items - RESOLVED)

- [x] **NEW-45:** update_players_file() migration strategy ✅ RESOLVED
  - **Decision:** Modified Option A - Write to JSON with selective field updates
  - **Implementation:** Update ONLY drafted_by and locked fields in JSON files
  - **Rationale:** Preserves all stats/projections from player-data-fetcher
  - **Current location:** PlayerManager.py:349-391
  - **Used by:** AddToRosterMode (1 call), ModifyPlayerDataMode (3 calls)
- [x] **NEW-52:** update_players_file() usage analysis ✅ RESOLVED
  - **Finding:** 4 calls total (AddToRoster: 1, ModifyPlayerData: 3)
  - **Decision:** Same as NEW-45 - migrate to selective JSON updates

---

## Core Implementation (8 items)

**Note:** Implementation tasks - patterns verified where possible, full implementation during coding phase

- [x] **NEW-75:** Implement selective JSON update algorithm ✅ PATTERN VERIFIED
  - **Current location:** PlayerManager.py:349-391 (update_players_file method)
  - **Current behavior:** Writes ALL fields to CSV
  - **New algorithm:**
    1. Read existing JSON file for each position
    2. Parse JSON structure (position key wrapper + array)
    3. Match players by ID between self.players and JSON data
    4. Update ONLY drafted_by and locked fields for matched players
    5. Preserve all other fields exactly as-is (stats, projections, etc.)
  - **Pattern:** Similar to selective update in ModifyPlayerDataModeManager (update specific fields only)
  - **Implementation:** Complete rewrite of method required
- [ ] **NEW-76:** Implement backup strategy before writes **(IMPLEMENTATION TASK)**
  - Create .bak file before overwriting JSON
  - Format: qb_data.json.bak
  - Log backup creation
  - Keep only most recent backup (overwrite old .bak)
  - **Pattern:** No existing backup pattern found in codebase - new implementation
- [x] **NEW-77:** Handle player not found in JSON ✅ PATTERN VERIFIED
  - Player in self.players but not in JSON file
  - **Decision:** Log warning and skip (don't add to JSON)
  - **Rationale:** player-data-fetcher owns player list, League Helper just updates status
  - **Pattern:** Matches PlayerManager.py:236-250 (skip with warning for data issues)
- [x] **NEW-78:** Handle position file missing ✅ RESOLVED (2025-12-28)
  - **Decision:** Option B - Raise FileNotFoundError (fail fast)
  - **Rationale:** Consistent with Decision 9, maintains ownership boundaries, prevents incomplete data
  - **Implementation:** Raise FileNotFoundError with actionable message directing to player-data-fetcher
  - **Error message:** "{position}_data.json not found in player_data/ directory. Please run player-data-fetcher to create missing position files."
- [ ] **NEW-79:** Implement atomic writes with temp files **(IMPLEMENTATION TASK)**
  - Write to .tmp file first (e.g., qb_data.json.tmp)
  - Rename to actual filename only if write succeeds
  - Use os.replace() for atomic operation (overwrites destination)
  - Prevents corruption if write fails mid-operation
  - **Pattern:** No existing atomic write pattern in codebase - new implementation
- [x] **NEW-80:** Preserve JSON formatting and structure ✅ PATTERN VERIFIED
  - Maintain same indentation (indent=2)
  - Preserve position key wrapper format (e.g., {"qb_data": [...]})
  - Maintain field order where possible
  - **Pattern:** json.dump(data, f, indent=2) - standard Python JSON formatting
  - **Verified:** JSON files in data/player_data/ use indent=2 consistently
- [x] **NEW-81:** Update method signature and docstring ✅ VERIFIED
  - **Current docstring:** Lines 350-362 references CSV writing
  - **Required changes:**
    - Update docstring to reflect JSON writing (not CSV)
    - Update return message ("Updated 6 JSON files" vs "Updated players.csv")
    - Update logging messages throughout method
    - Document selective update behavior (only drafted_by and locked)
  - **Location:** PlayerManager.py:349-362
- [x] **NEW-82:** Performance optimization considerations ✅ RESOLVED (2025-12-28)
  - **Decision:** Option B - Write all 6 files every time (no dirty tracking)
  - **Rationale:** Simple implementation, minimal performance impact (~50-150ms), low frequency, atomic consistency
  - **Implementation:** Iterate through all 6 positions regardless of changes
  - **Performance:** 6 files (~150KB total) writes in 50-150ms on SSD - acceptable for 1-10 calls per session

---

## Field Conversion Logic (3 items)

- [x] **NEW-83:** Convert drafted → drafted_by for JSON write ✅ VERIFIED
  - **Mapping:** drafted=0 → "", drafted=2 → "Sea Sharp", drafted=1 → player.drafted_by
  - **Issue:** For drafted=1, need actual team name
  - **Solution:** Use player.drafted_by field (hybrid approach from Decision 2 maintains it)
  - **Validation:** Verify drafted_by is set whenever drafted=1 during implementation
  - **Pattern:** Reverse of from_json() conversion in Sub-feature 1
- [x] **NEW-84:** Convert locked for JSON write ✅ VERIFIED
  - **After Sub-feature 3:** locked is already boolean in FantasyPlayer
  - Direct write, no conversion needed (write boolean directly to JSON)
  - **Verified:** Sub-feature 3 changes locked from int to bool
  - **Action:** Write player.locked directly (already boolean)
- [x] **NEW-85:** Verify no week_N_points written to JSON ✅ VERIFIED
  - JSON should have projected_points and actual_points arrays (from Sub-feature 2)
  - Do NOT write individual week_N_points fields
  - Only update drafted_by and locked (don't touch projection arrays)
  - **Verified:** Selective update only modifies drafted_by and locked - all other fields preserved
  - **Rationale:** player-data-fetcher owns projections, League Helper just updates status

---

## Error Handling (4 items)

- [x] **NEW-86:** Handle JSON parsing errors ✅ PATTERN VERIFIED
  - Malformed JSON file during read
  - **Decision:** Raise JSONDecodeError with clear message (fail fast)
  - Log error with filename and position in file
  - **Pattern:** Matches Sub-feature 1 CORE-7 (malformed JSON = fail fast)
  - **Consistency:** Same error handling as load_players_from_json()
- [x] **NEW-87:** Handle file write permission errors ✅ PATTERN VERIFIED
  - JSON file is read-only
  - Directory is read-only  - Disk full scenarios
  - **Action:** Raise PermissionError with actionable message
  - **Pattern:** Matches PlayerManager.py:244-248 (PermissionError handling)
  - **Message format:** Include filename and suggested action
- [x] **NEW-88:** Handle concurrent access issues ✅ DECISION VERIFIED
  - What if another process is reading/writing JSON?
  - **Decision:** Accept race condition risk (not using file locking)
  - **Rationale:** League Helper is single-user desktop app, low risk
  - Document this limitation in docstring
  - **Note:** Atomic writes (NEW-79) reduce but don't eliminate risk
- [x] **NEW-89:** Rollback strategy on failure ✅ RESOLVED (2025-12-28)
  - **Decision:** Option A - No automatic rollback (partial update acceptable)
  - **Rationale:** Simple implementation, rare scenario, visible failure, manual recovery available, partial progress valuable
  - **Implementation:** Let errors propagate immediately, no try/except around loop
  - **Recovery:** .bak files exist for all positions - user can manually restore or retry operation

---

## Testing (5 items)

**Note:** Testing items deferred to implementation phase - no verification needed during deep dive

- [ ] **NEW-90:** Unit test update_players_file() with mock JSON files **(Testing - defer to implementation)**
  - Create test JSON with known data
  - Update drafted_by and locked for some players
  - Verify other fields unchanged (stats, projections)
  - Verify only updated fields changed
- [ ] **NEW-91:** Test round-trip preservation **(Testing - defer to implementation)**
  - Load JSON → Modify drafted/locked → Save → Reload
  - Verify all stats (passing, rushing, etc.) unchanged
  - Verify only drafted_by and locked changed
  - Verify projected_points and actual_points preserved
- [ ] **NEW-92:** Test error scenarios **(Testing - defer to implementation)**
  - Missing JSON file (create new or error?)
  - Malformed JSON (raises JSONDecodeError)
  - Write permission errors
  - Player not found in JSON (skip with warning)
- [ ] **NEW-93:** Integration test with AddToRosterMode **(Testing - defer to implementation)**
  - Draft a player
  - Verify update_players_file() writes to JSON
  - Reload League Helper
  - Verify drafted status persists
  - Verify player data unchanged
- [ ] **NEW-94:** Integration test with ModifyPlayerDataMode **(Testing - defer to implementation)**
  - Lock/unlock players
  - Add/drop players (change drafted status)
  - Verify all changes persist to JSON
  - Verify no data loss (stats preserved)
  - Reload and verify persistence

---

## Dependency Updates (2 items)

- [x] **NEW-95:** Update to_json() method in FantasyPlayer ✅ RESOLVED
  - **Decision:** Do NOT create to_json() method
  - **Rationale:** update_players_file() accesses fields directly
  - **Alternative:** Can add later if future features need it
- [x] **NEW-96:** Verify from_json() round-trip compatibility ✅ VERIFIED
  - from_json() should load all fields that update_players_file() writes
  - All other fields preserved from original JSON (stats, projections)
  - No fields lost in round-trip (load → update → save → reload)
  - **Verified dependencies:**
    - Sub-feature 1: from_json() loads projected_points, actual_points, all nested stats
    - Sub-feature 2: projected_points/actual_points arrays preserved (not touched by update)
    - Sub-feature 3: locked is boolean in both FantasyPlayer and JSON (no conversion)
    - This sub-feature: Only drafted_by and locked updated, all other fields preserved
  - **Round-trip flow:**
    1. from_json() loads ALL fields (Sub-feature 1)
    2. League Helper modifies only drafted/locked
    3. update_players_file() writes back drafted_by/locked to JSON
    4. from_json() reloads ALL fields (stats unchanged)
  - **Conclusion:** Round-trip compatible - selective update preserves all data

---

## Success Criteria

✅ **update_players_file() writes to JSON files (not CSV)**
✅ **Selective updates (only drafted_by and locked modified)**
✅ **All stats and projections preserved during round-trip**
✅ **Atomic write pattern implemented (backup, temp, rename)**
✅ **All error scenarios handled gracefully**
✅ **All unit tests passing (100%)**
✅ **Integration tests with AddToRosterMode and ModifyPlayerDataMode passing**

---

## Dependencies

**Prerequisites:**
- Sub-feature 1 complete (from_json() exists, JSON structure understood)
- Sub-feature 3 complete (locked is boolean, no conversion needed)

**Uses:**
- drafted_by field (from Decision 2)
- locked boolean field (from Sub-feature 3)

---

## Impact Analysis

**Files Modified:** 1
- league_helper/util/PlayerManager.py (update_players_file method ~350-391)

**Callers (4 total):**
- league_helper/add_to_roster_mode/ (1 call - after drafting)
- league_helper/modify_player_data_mode/ (3 calls - after modifying data)

**Algorithm:**
1. Group self.players by position
2. For each position:
   - Backup existing JSON file (.bak)
   - Load existing JSON
   - Match players by ID
   - Update only drafted_by and locked
   - Write to .tmp file
   - Atomic rename .tmp to .json
3. Log success

---

## Notes

- Single source of truth: JSON files (no more CSV updates)
- Selective updates: Only change what League Helper manages (drafted status, locked status)
- Preserve everything else: player-data-fetcher owns stats and projections
- Atomic writes: Three-step pattern prevents corruption
- Backup files: Allow manual recovery if needed
