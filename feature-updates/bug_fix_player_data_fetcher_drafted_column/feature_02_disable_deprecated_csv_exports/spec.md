# Feature 2: Disable Deprecated CSV File Exports - Detailed Specification

**Created:** 2025-12-30 (Stage 1)
**Detailed:** 2025-12-30 (Stage 2 - Phase 2)

---

## Objective

Disable creation of deprecated `players.csv` and `players_projected.csv` files. These CSV files have been replaced by position JSON files (qb_data.json, rb_data.json, etc.) but are still being exported unconditionally.

---

## Root Cause Analysis

**Current State:**
- Player-data-fetcher creates `players.csv` and `players_projected.csv` on every run (unconditional exports)
- League helper system migrated to JSON loading (`load_players_from_json()`)
- CSV files are no longer read by any active code path
- Unnecessary file writes waste time and disk space

**Why This Matters:**
- Clean codebase (remove dead functionality)
- Faster execution (skip unnecessary exports)
- Reduce confusion (clear that JSON is the current system)

---

## Current System State (Verified in Phase 1)

### PlayerManager JSON Loading
**Status:** ✅ Already using JSON
- Default method: `load_players_from_json()` (line 139)
- CSV method: `load_players()` marked DEPRECATED (lines 146-161)
- Data source: Position JSON files (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)

### ProjectedPointsManager
**Status:** ✅ Deprecated and consolidated into PlayerManager
- Spec: `sub_feature_05_projected_points_manager_consolidation_spec.md`
- Projected points now from `player.projected_points` array (loaded from JSON)
- players_projected.csv NO LONGER USED

---

## Components Affected

### 1. players.csv Export Call - DISABLE
**File:** `player-data-fetcher/player_data_fetcher_main.py`
**Lines:** 352-356

**Current (CREATES FILE):**
```python
# Export to shared data/players.csv for draft helper integration
# This file is read by the draft helper to get current player projections
# Format: Full player data with all fields (id, name, team, position, fantasy_points, etc.)
shared_file = await self.exporter.export_to_data(data)
output_files.append(shared_file)
```

**Required Change (Option A - RECOMMENDED):**
```python
# DEPRECATED: Export to data/players.csv (replaced by position JSON files)
# League helper now uses load_players_from_json() to load from position JSON files
# Keeping this code commented for reference - can be removed in future cleanup
# shared_file = await self.exporter.export_to_data(data)
# output_files.append(shared_file)
```

**Alternative (Option B - Config Toggle):**
```python
# Export deprecated CSV files only if enabled (backward compatibility)
if self.settings.export_deprecated_csv:
    shared_file = await self.exporter.export_to_data(data)
    output_files.append(shared_file)
```

---

### 2. players_projected.csv Export Call - DISABLE
**File:** `player-data-fetcher/player_data_fetcher_main.py`
**Lines:** 358-368

**[UPDATED based on feature_01 implementation - 2025-12-31]**
**Note:** Line numbers may have shifted slightly due to feature_01 changes to player_data_exporter.py. Verify actual line numbers during implementation.

**Current (CREATES FILE):**
```python
# Export players_projected.csv with projection-only data
# Creates file from scratch with statSourceId=1 (ESPN projections) for ALL weeks
# Used by league helper for performance tracking against projections
try:
    projected_file = await self.exporter.export_projected_points_data(data)
    output_files.append(projected_file)
    self.logger.info("Exported players_projected.csv with projection-only data")
except Exception as e:
    # Error exporting projected points
    # Log error but don't fail entire export - this is a supplementary feature
    self.logger.error(f"Error exporting players_projected.csv: {e}")
```

**Required Change (Option A - RECOMMENDED):**
```python
# DEPRECATED: Export players_projected.csv (replaced by projected_points field in JSON)
# PlayerManager now uses player.projected_points array from JSON position files
# ProjectedPointsManager consolidated into PlayerManager (sub_feature_05 spec)
# Keeping this code commented for reference - can be removed in future cleanup
# try:
#     projected_file = await self.exporter.export_projected_points_data(data)
#     output_files.append(projected_file)
#     self.logger.info("Exported players_projected.csv with projection-only data")
# except Exception as e:
#     self.logger.error(f"Error exporting players_projected.csv: {e}")
```

**Alternative (Option B - Config Toggle):**
```python
# Export deprecated CSV files only if enabled (backward compatibility)
if self.settings.export_deprecated_csv:
    try:
        projected_file = await self.exporter.export_projected_points_data(data)
        output_files.append(projected_file)
    except Exception as e:
        self.logger.error(f"Error exporting players_projected.csv: {e}")
```

---

### 3. PLAYERS_CSV Constant (OPTIONAL - for Option C)
**File:** `player-data-fetcher/config.py`
**Line:** 37 **[UPDATED from 38 - feature_01 deleted PRESERVE_DRAFTED_VALUES at line 17, shifting all lines up by 1]**

**Current:**
```python
PLAYERS_CSV = '../data/players.csv'
```

**Options:**
- **Option A (Comment Out):** Leave as-is (no change needed, just commented code references it)
- **Option B (Config Toggle):** Add new config option EXPORT_DEPRECATED_CSV = False
- **Option C (Complete Removal):** Delete this line and remove import in exporter

---

### 4. SaveCalculatedPointsManager File Copy List - UPDATE ✅ REQUIRED
**File:** `league_helper/save_calculated_points_mode/SaveCalculatedPointsManager.py`
**Lines:** 131-132

**Current (WILL FAIL after deletion):**
```python
files_to_copy = [
    "players.csv",              # ← REMOVE (file won't exist)
    "players_projected.csv",    # ← REMOVE (file won't exist)
    "game_data.csv",
    "drafted_data.csv"
]
```

**Required Change:**
```python
files_to_copy = [
    "game_data.csv",
    "drafted_data.csv"
]
```

**Why:** SaveCalculatedPointsManager copies data files to historical snapshots. After deleting CSV exports, these files won't exist, causing copy to fail.

**Also Update Comment (Line 11):**
```python
# OLD: - Input data files (players.csv, configs/, team_data/, etc.)
# NEW: - Input data files (configs/, team_data/, etc.)
```

---

## Solution Comparison

| Aspect | Option A (Comment Out) | Option B (Config Toggle) | Option C (Complete Removal) |
|--------|------------------------|--------------------------|----------------------------|
| **Lines Changed** | ~17 | ~25 | ~200 |
| **Files Modified** | 1 | 2 | 4 |
| **Reversibility** | Easy (uncomment) | Easy (config True) | Hard (git restore) |
| **Code Cleanliness** | Medium (commented code) | Medium (dead config) | High (fully removed) |
| **Risk** | LOW | LOW | MEDIUM |
| **Complexity** | LOW | LOW-MEDIUM | MEDIUM |
| **Recommended?** | ✅ YES (safest) | ⚠️ Maybe (if rollback needed) | ❌ Not yet (too risky) |

---

## Chosen Approach: Option C (Complete Removal) ✅

**User Decision:** "C"

**Rationale:**
1. **Cleanest solution:** Removes all dead code (~200 lines)
2. **No confusion:** Clear that CSV system is deprecated
3. **Reduces codebase size:** Eliminates unused export methods
4. **Long-term maintainability:** No commented code to confuse future developers

**Risk Mitigation:**
- Thoroughly test all systems during Stage 5c (league helper, simulation)
- Integration tests will reveal any hidden dependencies
- 14 file references will be investigated during implementation

---

## Files Modified Summary (Option C - USER APPROVED)

**Investigation Complete:** Checked all 14 file references - only 1 requires code changes!

**[UPDATED based on feature_01 implementation - 2025-12-31]**

Line numbers shifted due to feature_01 deletions in player_data_exporter.py (~23 lines removed):
- export_to_data(): Now at line **775** (was 808)
- export_projected_points_data(): Now at line **877** (was 910)
- PLAYERS_CSV in config.py: Now at line **37** (was 38)

| File | Lines Changed | Complexity | Risk |
|------|---------------|------------|------|
| player_data_fetcher_main.py | -17 (delete export calls) | LOW | MEDIUM |
| player_data_exporter.py | -150 (delete 2 export methods at lines 775, 877) | LOW | MEDIUM |
| config.py | -1 (delete PLAYERS_CSV constant at line 37) | LOW | LOW |
| SaveCalculatedPointsManager.py | -2 (remove from files_to_copy) | LOW | LOW |
| Unit tests | +10 (verify CSVs NOT created) | LOW | LOW |

**Total Changes:** ~170 lines removed, ~10 lines added = ~180 lines total
**Overall Complexity:** LOW
**Overall Risk:** LOW (investigation confirms no hidden dependencies!)

**Key Finding:** Simulation system uses HISTORICAL sim_data snapshot files, NOT data/players.csv - no impact!

---

## Dependencies

**This feature depends on:**
- ✅ Feature 1 (data models updated - drafted_by field migration complete)
- ✅ Position JSON export system (already in place)
- ✅ PlayerManager JSON loading (already default)

**This feature blocks:**
- None

**This feature is independent of:**
- (No parallel features in this epic)

---

## Testing Strategy

### Unit Tests:
1. Test player-data-fetcher runs without errors
2. Verify players.csv NOT created in data/ folder
3. Verify players_projected.csv NOT created in data/ folder
4. Verify position JSON files STILL created successfully

### Integration Tests:
1. Run player-data-fetcher end-to-end
2. Launch league helper - verify loads from JSON successfully
3. Test all league helper modes:
   - Draft mode (add_to_roster)
   - Optimize mode (starter_helper)
   - Trade mode (trade_simulator)
   - Modify mode (modify_player_data)
4. Run simulation system - verify works without CSV files

### Verification Steps:
1. Note timestamps of existing players.csv and players_projected.csv (if present)
2. Run player-data-fetcher
3. Check timestamps - should NOT change (files not overwritten)
4. Check position JSON files - should have CURRENT timestamp

---

## Edge Cases

### Edge Case 1: Simulation System CSV Dependency
**Scenario:** simulation/ folder has 7 file references to these CSVs
**Risk:** Simulation might fail if CSVs not present
**Mitigation:** Integration test simulation system after disabling exports
**Status:** TO INVESTIGATE in Phase 3 (ask user if simulation tested)

### Edge Case 2: ModifyPlayerDataMode CSV Writing
**Scenario:** ModifyPlayerDataModeManager.py might write changes to CSV
**Risk:** Mode might expect to write back to deprecated CSV
**Mitigation:** Verify modify mode works with JSON only
**Status:** TO INVESTIGATE in Phase 3

### Edge Case 3: Old CSV Files Still Present
**Scenario:** Existing players.csv and players_projected.csv from previous runs
**Risk:** Code might read old stale data if present
**Mitigation:** Document that old CSVs can be safely deleted
**Status:** DOCUMENT in implementation guide

---

## File References Investigation Results ✅

**Investigation Complete** - See `research/FILE_REFERENCES_INVESTIGATION.md` for full details

**Summary:**
- **14 files investigated** (7 league_helper, 7 simulation)
- **13 files:** Comments/docstrings/deprecated code only (NO changes needed)
- **1 file requires code change:** SaveCalculatedPointsManager.py

**Key Findings:**
1. **Simulation system NOT affected** - uses historical sim_data snapshots, not data/players.csv
2. **PlayerManager already uses JSON** - deprecated load_players() method not called by default
3. **ProjectedPointsManager already deprecated** - class consolidated into PlayerManager
4. **SaveCalculatedPointsManager** - only file that needs updating (remove from copy list)

---

## Implementation Checklist (HIGH-LEVEL)

**[UPDATED based on feature_01 implementation - 2025-12-31]**

**Option C (USER APPROVED) - Investigation Complete:**
1. DELETE lines 352-368 in player_data_fetcher_main.py (both export calls)
2. DELETE export_to_data() method in player_data_exporter.py (**line 775** - updated from 808)
3. DELETE export_projected_points_data() method in player_data_exporter.py (**line 877** - updated from 910)
4. DELETE PLAYERS_CSV constant in config.py (**line 37** - updated from 38)
5. REMOVE import of PLAYERS_CSV in player_data_exporter.py (if present)
6. UPDATE SaveCalculatedPointsManager.py - remove players.csv from files_to_copy (lines 131-132)
7. UPDATE SaveCalculatedPointsManager.py comment (line 11) - remove players.csv reference
8. UPDATE unit tests to verify CSVs NOT created
9. RUN integration tests (league helper all modes, simulation)
10. DOCUMENT that old CSV files can be deleted

**Estimated Total Tasks:** ~12 items (reduced after investigation confirmed no hidden dependencies!)

---

## Open Questions (See checklist.md)

**All questions resolved:**
1. ~~Should we use Option A (comment) vs Option B (config) vs Option C (remove)?~~ ✅ Option C (Complete Removal)
2. ~~Should we investigate the 14 file references immediately or in separate cleanup?~~ ✅ Investigated now - only 1 needs changes
3. ~~Does simulation system actually depend on these CSV files?~~ ✅ NO - uses historical sim_data snapshots
4. ~~Should old players.csv and players_projected.csv be deleted automatically?~~ ✅ Option C (Do Nothing)

---

**Status:** Spec complete with all decisions finalized (Stage 2 complete)
**Next:** Phase 4 & 5 complete, ready for Stage 3 (Cross-Feature Sanity Check) after all features done
