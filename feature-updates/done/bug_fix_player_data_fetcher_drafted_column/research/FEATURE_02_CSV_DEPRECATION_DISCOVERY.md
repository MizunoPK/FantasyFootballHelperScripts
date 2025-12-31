# Feature 02: Disable Deprecated CSV File Exports - Discovery Findings

**Research Date:** 2025-12-30
**Researcher:** Agent
**Feature:** feature_02_disable_deprecated_csv_exports

---

## Problem Statement

**Root Cause:**
- `players.csv` and `players_projected.csv` are still being exported by player-data-fetcher
- League helper system has migrated to JSON position files (qb_data.json, rb_data.json, etc.)
- CSV files are deprecated but still being created, causing unnecessary file writes

**Goal:**
- Disable creation of deprecated CSV files
- Ensure no system dependencies are broken
- Clean approach preferred (config option or code removal)

---

## Components Identified

### 1. players.csv Export
**File:** `player-data-fetcher/player_data_fetcher_main.py`
**Lines:** 352-356

**Current State:**
```python
# Export to shared data/players.csv for draft helper integration
# This file is read by the draft helper to get current player projections
# Format: Full player data with all fields (id, name, team, position, fantasy_points, etc.)
shared_file = await self.exporter.export_to_data(data)
output_files.append(shared_file)
```

**Export Method:** `DataExporter.export_to_data()` (player_data_exporter.py:808-845)
**File Created:** `data/players.csv`
**Control:** UNCONDITIONAL - always runs, not controlled by any config

---

### 2. players_projected.csv Export
**File:** `player-data-fetcher/player_data_fetcher_main.py`
**Lines:** 358-368

**Current State:**
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

**Export Method:** `DataExporter.export_projected_points_data()` (player_data_exporter.py:910-958)
**File Created:** `data/players_projected.csv`
**Control:** UNCONDITIONAL (but wrapped in try/except)

---

### 3. PLAYERS_CSV Constant
**File:** `player-data-fetcher/config.py`
**Line:** 38

**Current State:**
```python
PLAYERS_CSV = '../data/players.csv'
```

**Usage:** Referenced in `DataExporter.export_to_data()` method

---

## Dependency Analysis

### PlayerManager (league_helper/util/PlayerManager.py)

**Current Loading Method (line 139):**
```python
self.load_players_from_json()
```

**Deprecated CSV Method (lines 146-161):**
```python
def load_players(self) -> bool:
    """
    DEPRECATED: Use load_players_from_json() instead.

    This method loads player data from the old players.csv format.
    It is maintained for backward compatibility only.
    """
```

**Status:** ✅ PlayerManager already uses JSON loading by default
- `load_players()` marked DEPRECATED
- `load_players_from_json()` is the current method
- Position JSON files (qb_data.json, rb_data.json, etc.) are the data source

---

### ProjectedPointsManager (league_helper/util/ProjectedPointsManager.py)

**Status:** ✅ Class DEPRECATED and consolidated into PlayerManager
- Spec reference: `sub_feature_05_projected_points_manager_consolidation_spec.md`
- PlayerManager now handles projected points via `player.projected_points` array
- Projected points loaded from position JSON files, NOT players_projected.csv

**Evidence from PlayerManager (lines 119, 788, 810):**
```python
# Line 119: Pass self (PlayerManager) instead of ProjectedPointsManager for consolidated projection access
# Line 788: Spec: sub_feature_05_projected_points_manager_consolidation_spec.md
# Line 810: Improvement over original ProjectedPointsManager: raise ValueError instead of None
# Line 816: if not player.projected_points or len(player.projected_points) < week:
```

---

### Other References Found

**14 files reference these CSV files:**
- 7 in league_helper/
- 7 in simulation/

**Assessment:** Likely dead code or deprecated paths. Need to verify:
1. Are these just old comments/docstrings?
2. Are these fallback paths that never execute?
3. Are these deprecated methods that aren't called?

**Example from grep results:**
- `league_helper\modify_player_data_mode\ModifyPlayerDataModeManager.py`
- `league_helper\save_calculated_points_mode\SaveCalculatedPointsManager.py`
- `league_helper\util\DraftedDataWriter.py`
- `simulation\win_rate\SimulatedOpponent.py`
- `simulation\win_rate\SimulationManager.py`

---

## Data Flow Analysis

**Current (WITH deprecated CSV exports):**
```
1. ESPN API
   ↓
2. ESPNPlayerData (drafted_by: str) [fixed by Feature 1]
   ↓
3. FantasyPlayer objects
   ↓
4. DataExporter exports in parallel:
   a. Position JSON files → qb_data.json, rb_data.json, etc. (CURRENT SYSTEM)
   b. players.csv (DEPRECATED - but still created)
   c. players_projected.csv (DEPRECATED - but still created)
   d. Other formats (if enabled): Excel, etc.
```

**Target (WITHOUT deprecated CSV exports):**
```
1. ESPN API
   ↓
2. ESPNPlayerData (drafted_by: str) [fixed by Feature 1]
   ↓
3. FantasyPlayer objects
   ↓
4. DataExporter exports:
   a. Position JSON files → qb_data.json, rb_data.json, etc. (CURRENT SYSTEM)
   b. Other formats (if enabled): Excel, etc.
   c. [REMOVED] players.csv
   d. [REMOVED] players_projected.csv
```

---

## Solution Options

### Option A: Comment Out Export Calls
**Approach:** Comment out lines 355-356 and 362-368 in player_data_fetcher_main.py

**Pros:**
- Simplest change (just comment out 2 blocks)
- Easy to reverse if needed (uncomment)
- No config changes needed

**Cons:**
- Leaves dead code in place
- Comments may confuse future developers
- Not as clean as complete removal

**Implementation:**
```python
# DEPRECATED: Export to data/players.csv (replaced by position JSON files)
# shared_file = await self.exporter.export_to_data(data)
# output_files.append(shared_file)

# DEPRECATED: Export players_projected.csv (replaced by position JSON projected_points field)
# try:
#     projected_file = await self.exporter.export_projected_points_data(data)
#     output_files.append(projected_file)
#     self.logger.info("Exported players_projected.csv with projection-only data")
# except Exception as e:
#     self.logger.error(f"Error exporting players_projected.csv: {e}")
```

---

### Option B: Add Config Toggle
**Approach:** Create new config option `EXPORT_DEPRECATED_CSV = False` and wrap calls

**Pros:**
- Provides easy rollback mechanism (set to True if needed)
- Explicit control over deprecated functionality
- Clear documentation via config comments

**Cons:**
- More code changes (config.py + main.py)
- Adds complexity for deprecated feature
- May confuse users about why option exists

**Implementation:**

`config.py`:
```python
# Deprecated CSV export control (for backward compatibility only)
# Set to False to disable creation of players.csv and players_projected.csv
# Modern systems use position JSON files (qb_data.json, rb_data.json, etc.)
EXPORT_DEPRECATED_CSV = False
```

`player_data_fetcher_main.py`:
```python
# Export deprecated CSV files only if enabled (backward compatibility)
if self.settings.export_deprecated_csv:
    shared_file = await self.exporter.export_to_data(data)
    output_files.append(shared_file)

    try:
        projected_file = await self.exporter.export_projected_points_data(data)
        output_files.append(projected_file)
    except Exception as e:
        self.logger.error(f"Error exporting players_projected.csv: {e}")
```

---

### Option C: Complete Removal
**Approach:** Delete export calls AND export methods entirely

**Pros:**
- Cleanest solution (no dead code)
- Reduces codebase size (~150 lines removed)
- No confusion about what's deprecated

**Cons:**
- Hardest to reverse (requires code restore from git)
- May break unknown dependencies (risky)
- More files to modify (main + exporter)

**Files to modify:**
1. `player_data_fetcher_main.py` - Remove lines 352-368
2. `player_data_exporter.py` - Remove export_to_data() (lines 808-845)
3. `player_data_exporter.py` - Remove export_projected_points_data() (lines 910-958)
4. `config.py` - Remove PLAYERS_CSV constant (line 38)

---

## Recommended Approach

**Recommendation: Option A (Comment Out)**

**Rationale:**
1. **Safest:** No risk of breaking unknown dependencies
2. **Reversible:** Easy to uncomment if issues discovered
3. **Minimal changes:** Only touch main.py file
4. **Aligns with Feature 1:** Feature 1 removed PRESERVE_DRAFTED_VALUES dead code, this is similar
5. **User can decide later:** Can move to Option C (complete removal) after verification

**Verification Steps:**
1. Comment out export calls
2. Run player data fetcher end-to-end
3. Verify position JSON files still created
4. Verify league helper loads from JSON successfully
5. Check data/ folder - confirm players.csv and players_projected.csv NOT created

---

## Dependencies

**This feature depends on:**
- ✅ Feature 1 (data models updated - drafted_by field migration complete)
- ✅ Position JSON export system (qb_data.json, rb_data.json, etc.) - already in place
- ✅ PlayerManager JSON loading (load_players_from_json) - already default

**This feature blocks:**
- None

**This feature is independent of:**
- Other epic features

---

## Files Affected Summary

| File | Lines | Change Type | Risk |
|------|-------|-------------|------|
| player_data_fetcher_main.py | 352-368 (17 lines) | Comment out | LOW |
| (Optional) config.py | N/A | No changes needed | NONE |
| (Optional) player_data_exporter.py | N/A | No changes needed | NONE |

**Total Estimated Changes:** ~17 lines commented out (Option A)

---

## Edge Cases Identified

### Edge Case 1: Simulation System Still Using CSV
**Scenario:** simulation/ folder has 7 file references to these CSVs
**Risk:** Simulation might fail if CSVs not present
**Mitigation:** Test simulation system after disabling exports

### Edge Case 2: ModifyPlayerDataMode Writing to CSV
**Scenario:** ModifyPlayerDataModeManager.py references players.csv
**Risk:** Mode might try to write changes back to deprecated CSV
**Mitigation:** Verify modify mode works with JSON only

### Edge Case 3: DraftedDataWriter CSV Dependency
**Scenario:** DraftedDataWriter.py references players.csv
**Risk:** Drafted data tracking might break
**Mitigation:** Verify DraftedDataWriter uses JSON or separate drafted_data.csv

---

## Testing Strategy

### Unit Tests:
1. Test player-data-fetcher runs without creating players.csv
2. Test player-data-fetcher runs without creating players_projected.csv
3. Test position JSON files still created successfully

### Integration Tests:
1. Run player-data-fetcher end-to-end
2. Launch league helper - verify loads from JSON
3. Test all 4 league helper modes (draft, optimize, trade, modify)
4. Run simulation system - verify works without CSVs

### Verification:
1. Check data/ folder before run (note existing CSV timestamps)
2. Run player-data-fetcher
3. Check data/ folder after run (confirm CSVs not updated)
4. Verify position JSON files have latest timestamp

---

## Next Steps for Phase 2 (Update Spec)

1. Create `spec.md` with detailed component changes
2. Create `checklist.md` with open questions:
   - Use Option A (comment) vs Option B (config) vs Option C (remove)?
   - Should we clean up the 14 dead code references immediately or separately?
   - Verify simulation system doesn't depend on CSVs?

---

**Research Complete:** Components identified, dependency analysis complete, solution options documented.
