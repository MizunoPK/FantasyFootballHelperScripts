# Iteration 5: End-to-End Data Flow

**Date:** 2025-12-31
**Feature:** Feature 01 - File Persistence Issues
**Round:** 1 (TODO Creation)
**Iteration:** 5 of 8

---

## Purpose

Trace data from entry point through all transformations to output. Verify no gaps in data flow.

---

## Entry Point

**User Action:** Modify player data in Modify Player Data mode

**Entry Points (3 possible user actions):**
1. Mark player as drafted: ModifyPlayerDataModeManager._mark_player_as_drafted()
2. Drop player: ModifyPlayerDataModeManager._drop_player()
3. Lock player: ModifyPlayerDataModeManager._lock_player()

**Data Input:**
- Player selection from user
- Team name (for drafted_by field)
- Lock status (for locked field)

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ ENTRY POINT: User modifies player in Modify Player Data mode   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: User selects action (draft / drop / lock)              │
│                                                                 │
│ ModifyPlayerDataModeManager methods:                           │
│ - _mark_player_as_drafted(player) → sets player.drafted_by     │
│ - _drop_player(player) → sets player.drafted_by = ""           │
│ - _lock_player(player) → toggles player.locked                 │
│                                                                 │
│ Data State: In-memory FantasyPlayer objects modified           │
│ Files State: JSON files NOT YET updated                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: ModifyPlayerDataModeManager calls persist method       │
│                                                                 │
│ Code: self.player_manager.update_players_file()                │
│                                                                 │
│ Input: self.players (List[FantasyPlayer])                      │
│ - All players in memory (not just modified ones)               │
│ - Modified players have updated drafted_by/locked fields       │
│                                                                 │
│ Data State: List[FantasyPlayer] passed to PlayerManager        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: update_players_file() groups players by position       │
│                                                                 │
│ Code: PlayerManager.update_players_file() lines 481-493        │
│                                                                 │
│ Data Transformation:                                            │
│ List[FantasyPlayer] → Dict[str, List[FantasyPlayer]]           │
│                                                                 │
│ Example:                                                        │
│ {                                                               │
│   "QB": [player1, player2, ...],                               │
│   "RB": [player3, player4, ...],                               │
│   "WR": [player5, player6, ...],                               │
│   "TE": [player7, player8, ...],                               │
│   "K": [player9, player10, ...],                               │
│   "DST": [player11, player12, ...]                             │
│ }                                                               │
│                                                                 │
│ **PRESERVED by Task 1** (no changes to this logic)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: For each position, read existing JSON file             │
│                                                                 │
│ Code: PlayerManager.update_players_file() lines 500-520        │
│                                                                 │
│ Loop: for position in ['qb', 'rb', 'wr', 'te', 'k', 'dst']    │
│                                                                 │
│ Data Transformation:                                            │
│ JSON file on disk → Python dict                                │
│                                                                 │
│ Example (qb_data.json):                                         │
│ {                                                               │
│   "qb_data": [                                                  │
│     {                                                           │
│       "id": "12345",                                            │
│       "name": "Patrick Mahomes",                                │
│       "drafted_by": "",  // OLD VALUE from disk                │
│       "locked": false,   // OLD VALUE from disk                │
│       "projected_points": [...],                                │
│       ...                                                       │
│     },                                                          │
│     ...                                                         │
│   ]                                                             │
│ }                                                               │
│                                                                 │
│ **PRESERVED by Task 1** (no changes to this logic)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: Extract players array from position key                │
│                                                                 │
│ Code: PlayerManager.update_players_file() lines 520-530        │
│                                                                 │
│ Data Transformation:                                            │
│ Dict[position_key, List[player_dicts]] → List[player_dicts]    │
│                                                                 │
│ Example:                                                        │
│ players_array = json_data["qb_data"]  // Extract QBs           │
│                                                                 │
│ **PRESERVED by Task 1** (no changes to this logic)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: Selectively update drafted_by and locked fields        │
│                                                                 │
│ Code: PlayerManager.update_players_file() lines 530-551        │
│                                                                 │
│ Logic: For each player dict in JSON:                           │
│   1. Find matching FantasyPlayer in self.players (by ID)       │
│   2. If match found:                                            │
│      - player_dict["drafted_by"] = memory_player.drafted_by    │
│      - player_dict["locked"] = memory_player.locked            │
│   3. ALL OTHER FIELDS PRESERVED (projections, stats, etc.)     │
│                                                                 │
│ Data Transformation:                                            │
│ OLD player_dict + NEW drafted_by/locked → UPDATED player_dict  │
│                                                                 │
│ Example:                                                        │
│ {                                                               │
│   "id": "12345",                                                │
│   "name": "Patrick Mahomes",                                    │
│   "drafted_by": "Sea Sharp",  // ← UPDATED from memory         │
│   "locked": false,            // ← UPDATED from memory         │
│   "projected_points": [...],  // ← PRESERVED from JSON         │
│   ...                                                           │
│ }                                                               │
│                                                                 │
│ **PRESERVED by Task 1** (no changes to this logic)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 7: Create .bak backup file **[BUG - TO BE REMOVED]**      │
│                                                                 │
│ Code: PlayerManager.update_players_file() lines 553-556        │
│                                                                 │
│ Logic:                                                          │
│ backup_path = json_path.with_suffix('.bak')                    │
│ if json_path.exists():                                          │
│     shutil.copy2(json_path, backup_path)                       │
│                                                                 │
│ Data Transformation:                                            │
│ qb_data.json → qb_data.bak (UNWANTED SIDE EFFECT)              │
│                                                                 │
│ **REMOVED by Task 1** (DELETE these 4 lines)                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 8: Write updated data to .tmp file                        │
│                                                                 │
│ Code: PlayerManager.update_players_file() lines 558-563        │
│                                                                 │
│ Logic:                                                          │
│ json_data_to_write = {position_key: players_array}             │
│ tmp_path = json_path.with_suffix('.tmp')                       │
│ with open(tmp_path, 'w', encoding='utf-8') as f:               │
│     json.dump(json_data_to_write, f, indent=2)                 │
│                                                                 │
│ Data Transformation:                                            │
│ Python dict → JSON text → .tmp file on disk                    │
│                                                                 │
│ Example (qb_data.tmp):                                          │
│ {                                                               │
│   "qb_data": [                                                  │
│     {                                                           │
│       "id": "12345",                                            │
│       "name": "Patrick Mahomes",                                │
│       "drafted_by": "Sea Sharp",  // NEW VALUE                 │
│       "locked": false,                                          │
│       ...                                                       │
│     }                                                           │
│   ]                                                             │
│ }                                                               │
│                                                                 │
│ **PRESERVED by Task 1** (no changes to this logic)             │
│ **VERIFIED by Task 9** (atomic write pattern on Windows)       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 9: Atomically replace .json file with .tmp file           │
│                                                                 │
│ Code: PlayerManager.update_players_file() line 566             │
│                                                                 │
│ Logic:                                                          │
│ tmp_path.replace(json_path)                                    │
│                                                                 │
│ Data Transformation:                                            │
│ qb_data.tmp → qb_data.json (atomic replace)                    │
│                                                                 │
│ Platform Behavior:                                              │
│ - POSIX: Guaranteed atomic                                      │
│ - Windows: NOT guaranteed atomic (may fail if file open)       │
│                                                                 │
│ **PRESERVED by Task 1** (no changes to this logic)             │
│ **VERIFIED by Task 9** (integration test on win32)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ OUTPUT: Updated JSON files on disk                             │
│                                                                 │
│ Files:                                                          │
│ - data/player_data/qb_data.json (UPDATED)                      │
│ - data/player_data/rb_data.json (UPDATED)                      │
│ - data/player_data/wr_data.json (UPDATED)                      │
│ - data/player_data/te_data.json (UPDATED)                      │
│ - data/player_data/k_data.json (UPDATED)                       │
│ - data/player_data/dst_data.json (UPDATED)                     │
│                                                                 │
│ Side Effects (BEFORE Task 1):                                   │
│ - qb_data.bak, rb_data.bak, ... (UNWANTED)                     │
│                                                                 │
│ Side Effects (AFTER Task 1):                                    │
│ - NO .bak files created ✅                                      │
│ - NO .tmp files left behind ✅                                  │
│                                                                 │
│ **VERIFIED by Task 13** (no .bak files in real filesystem)     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ DOWNSTREAM CONSUMPTION: Modifications visible immediately      │
│                                                                 │
│ Next Operations:                                                │
│ - User returns to main menu                                     │
│ - LeagueHelperManager reloads player data from JSON files      │
│ - Modified drafted_by and locked fields are visible            │
│ - Other modes (Draft, Trade, Lineup) see updated data          │
│                                                                 │
│ **VERIFIED by Task 11** (changes persist immediately)          │
│ **VERIFIED by Task 12** (changes persist across restarts)      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Verification

### Gap Analysis

**Step 1 → Step 2:**
- ✅ In-memory FantasyPlayer objects modified → passed to update_players_file()
- ✅ No gap: Direct method call

**Step 2 → Step 3:**
- ✅ List[FantasyPlayer] → Dict[position, List[FantasyPlayer]]
- ✅ No gap: Grouping logic preserves all players

**Step 3 → Step 4:**
- ✅ For each position → read corresponding JSON file
- ✅ No gap: Loop covers all 6 positions

**Step 4 → Step 5:**
- ✅ JSON file content → players array extracted
- ✅ No gap: Dict key access

**Step 5 → Step 6:**
- ✅ OLD player dicts + NEW memory values → UPDATED player dicts
- ✅ No gap: ID matching ensures correct updates

**Step 6 → Step 7:**
- ⚠️ **BUG:** Creates .bak files (TO BE REMOVED)
- ✅ Task 1 removes this step

**Step 7 → Step 8:**
- ✅ Updated player dicts → .tmp file
- ✅ No gap: JSON serialization

**Step 8 → Step 9:**
- ✅ .tmp file → .json file (atomic replace)
- ✅ No gap: Path.replace() operation

**Step 9 → Output:**
- ✅ Atomic replace completes → JSON files updated
- ✅ No gap: File operation completes

**Output → Downstream:**
- ✅ JSON files updated → reload sees changes
- ✅ No gap: File-based persistence

---

## Data Transformations Summary

| Step | Input Format | Output Format | Transformation Type |
|------|--------------|---------------|---------------------|
| 1 | User input | Modified FantasyPlayer objects | Direct field assignment |
| 2 | List[FantasyPlayer] | Same list | Pass-by-reference |
| 3 | List[FantasyPlayer] | Dict[str, List[FantasyPlayer]] | Grouping by position |
| 4 | JSON file | Python dict | JSON deserialization |
| 5 | Dict[position_key, List] | List[player_dicts] | Dict key extraction |
| 6 | OLD dict + NEW values | UPDATED dict | Selective field merge |
| 7 | .json file | .bak file | **BUG - File copy (REMOVED)** |
| 8 | Python dict | .tmp file | JSON serialization |
| 9 | .tmp file | .json file | Atomic file replace |

---

## Test Coverage for Data Flow

**End-to-End Flow Tests:**

**Entry to Output (Full Flow):**
- ✅ Task 10: Integration Test - JSON File Contents Match Expected Format
  - Verifies: Step 1 → Step 9 (complete flow)
  - Confirms: drafted_by and locked fields persist correctly

**Immediate Persistence:**
- ✅ Task 11: Integration Test - Changes Persist Immediately
  - Verifies: Output → Downstream consumption (same process)
  - Confirms: Changes visible right after update_players_file()

**Cross-Restart Persistence:**
- ✅ Task 12: Integration Test - Changes Persist Across Restarts
  - Verifies: Output → Downstream consumption (new process)
  - Confirms: Changes survive app restart

**Atomic Write Pattern:**
- ✅ Task 9: Integration Test - Atomic Write Pattern on Windows
  - Verifies: Step 8 → Step 9 (tmp → json atomic replace)
  - Confirms: Path.replace() works correctly on win32

**Field-Level Persistence:**
- ✅ Task 5: Unit Test - drafted_by Persistence (Mocked)
  - Verifies: Step 6 (drafted_by field update)
- ✅ Task 6: Unit Test - locked Persistence (Mocked)
  - Verifies: Step 6 (locked field update)

**Bug Fix Verification:**
- ✅ Task 7: Unit Test - NO .bak Files Created (Mocked)
  - Verifies: Step 7 REMOVED (no shutil.copy2 call)
- ✅ Task 13: Integration Test - NO .bak Files in Real Filesystem
  - Verifies: Step 7 REMOVED (no .bak files on disk)

---

## Critical Data Flow Points

**Point 1: Selective Field Update (Step 6)**
- CRITICAL: Only drafted_by and locked fields updated
- All other fields (projections, stats) PRESERVED
- **Why:** player-data-fetcher creates JSON with projections, we don't want to overwrite them

**Point 2: Atomic Write Pattern (Steps 8-9)**
- CRITICAL: Crash safety without needing .bak files
- Writes to .tmp first, then atomic replace
- **Platform Risk:** Windows Path.replace() NOT guaranteed atomic
- **Mitigation:** Task 9 integration test verifies on win32

**Point 3: .bak File Creation (Step 7 - REMOVED)**
- CRITICAL: User explicitly does NOT want .bak files
- These files clutter directory and aren't in .gitignore
- **Fix:** Task 1 removes lines 553-556

---

## Data Flow Gaps (NONE FOUND)

**All gaps verified as closed.**

**No additional E2E tests needed** - existing test tasks (9-13) cover complete data flow.

---

## Next Steps

**Iteration 5 COMPLETE**

**Next:** Iteration 6 - Error Handling Scenarios

---

**END OF ITERATION 5**
