# Cross-Feature Sanity Check

**Date:** 2025-12-30
**Epic:** bug_fix_player_data_fetcher_drafted_column
**Features Compared:** 2 features

---

## Comparison Matrix

### Category 1: Data Structures

| Feature | Data Modified | Field Names | Data Types | File Changes | Conflicts? |
|---------|--------------|-------------|------------|--------------|------------|
| Feature 1 (Update Data Models) | ESPNPlayerData model | `drafted: int` → `drafted_by: str` | int → str migration | player_data_models.py, espn_client.py, player_data_exporter.py | ❌ None |
| Feature 2 (Disable CSV Exports) | No data model changes | N/A (removes file exports) | N/A | player_data_fetcher_main.py, player_data_exporter.py, SaveCalculatedPointsManager.py | ❌ None |

**Analysis:**
- Feature 1: Changes data model field (drafted → drafted_by)
- Feature 2: Removes CSV export code (no model changes)
- **Conflict Check:** ❌ No conflicts - different concerns (data vs export)

---

### Category 2: Interfaces & Dependencies

| Feature | Depends On | Modifies Methods | Expected Interfaces | Conflicts? |
|---------|-----------|------------------|-------------------|------------|
| Feature 1 | FantasyPlayer (already has drafted_by field), DraftedRosterManager (already uses drafted_by) | `_espn_player_to_fantasy_player()`, `_get_drafted_by()`, removes `_load_existing_drafted_values()` | FantasyPlayer constructor accepts `drafted_by: str` | ❌ None |
| Feature 2 | Feature 1 MUST complete first (depends on data model migration) | Deletes `export_to_data()`, `export_projected_points_data()`, removes calls in main | No interface expectations (removing code) | ❌ None |

**Analysis:**
- Feature 1: Migrates data models to use drafted_by field
- Feature 2: **Explicitly depends on Feature 1** (cannot run CSV exports with broken data models)
- **Dependency Chain:** Feature 1 MUST complete before Feature 2
- **Conflict Check:** ❌ No conflicts - clean dependency

---

### Category 3: File Locations & Naming

| Feature | Creates Files | Deletes Files | File Locations | Naming Conventions | Conflicts? |
|---------|--------------|---------------|----------------|-------------------|------------|
| Feature 1 | None (modifies existing code) | Removes PRESERVE_DRAFTED_VALUES config, removes `_load_existing_drafted_values()` method | player-data-fetcher/ module | N/A | ❌ None |
| Feature 2 | None (removes file creation) | Removes creation of `data/players.csv` and `data/players_projected.csv` | player-data-fetcher/ module | N/A | ❌ None |

**Analysis:**
- Feature 1: No file creation/deletion (code changes only)
- Feature 2: **Stops creating** data/players.csv and data/players_projected.csv
- **Both touch player-data-fetcher module** but different files:
  - Feature 1: player_data_models.py, espn_client.py, player_data_exporter.py (conversion logic)
  - Feature 2: player_data_fetcher_main.py, player_data_exporter.py (export logic), SaveCalculatedPointsManager.py (file copy list)
- **Conflict Check:** ❌ No conflicts - different files (one overlap: player_data_exporter.py but different sections)

---

### Category 4: Configuration Keys

| Feature | Config Keys Modified | Config File | Key Conflicts? | Conflicts? |
|---------|---------------------|-------------|----------------|------------|
| Feature 1 | Removes `PRESERVE_DRAFTED_VALUES`, updates `EXPORT_COLUMNS` ('drafted' → 'drafted_by') | player-data-fetcher/config.py | None | ❌ None |
| Feature 2 | Removes `PLAYERS_CSV` constant | player-data-fetcher/config.py | None | ❌ None |

**Analysis:**
- Feature 1: Removes PRESERVE_DRAFTED_VALUES, updates EXPORT_COLUMNS
- Feature 2: Removes PLAYERS_CSV constant
- **Both modify config.py** but different lines:
  - Feature 1: Line 17 (PRESERVE_DRAFTED_VALUES delete), Line 84 (EXPORT_COLUMNS update)
  - Feature 2: Line 38 (PLAYERS_CSV delete)
- **Conflict Check:** ❌ No conflicts - different config keys

---

### Category 5: Algorithms & Logic

| Feature | Algorithm Type | Logic Changes | Execution Order | Conflicts? |
|---------|---------------|---------------|-----------------|------------|
| Feature 1 | Data transformation | Changes ESPNPlayerData → FantasyPlayer conversion from `drafted: int` to `drafted_by: str`, simplifies `_get_drafted_by()` to return field directly | Runs during player data fetch (data creation) | ❌ None |
| Feature 2 | File export removal | Deletes CSV export calls, removes export methods entirely | Runs during player data fetch (export phase) | ❌ None |

**Analysis:**
- Feature 1: Affects **data creation** phase (model conversion)
- Feature 2: Affects **export phase** (file writing)
- **Execution Flow:**
  1. ESPN API fetch
  2. ESPNPlayerData creation (Feature 1 changes this)
  3. FantasyPlayer conversion (Feature 1 changes this)
  4. Position JSON export (unchanged)
  5. ~~CSV export~~ (Feature 2 removes this)
- **Sequential dependency:** Feature 1 must complete first (data model must be correct before disabling CSV exports)
- **Conflict Check:** ❌ No conflicts - sequential phases

---

### Category 6: Testing Assumptions

| Feature | Test Data Needs | Mock Dependencies | Integration Points | Conflicts? |
|---------|----------------|-------------------|-------------------|------------|
| Feature 1 | ESPNPlayerData with drafted_by field, FantasyPlayer objects, position JSON files | Mock DraftedRosterManager (already uses drafted_by) | Position JSON export must work with drafted_by field | ❌ None |
| Feature 2 | Position JSON files must be created, CSV files must NOT be created | SaveCalculatedPointsManager file copy test | League helper must load from JSON successfully, simulation system must use sim_data/ snapshots | ❌ None |

**Analysis:**
- Feature 1: Tests data model migration (drafted → drafted_by)
- Feature 2: Tests CSV export removal (files not created)
- **Integration Testing:**
  - Both features need end-to-end player-data-fetcher test
  - Feature 1: Verify position JSON has drafted_by field
  - Feature 2: Verify players.csv and players_projected.csv NOT created
  - Combined: Verify league helper loads from JSON successfully
- **Conflict Check:** ❌ No conflicts - complementary testing

---

## Summary: Conflicts Identified

**Total Conflicts Found:** 0

✅ **NO CONFLICTS** - All features aligned

**Analysis:**
- Feature 1 and Feature 2 have clean separation of concerns
- Feature 1: Data model migration (drafted → drafted_by)
- Feature 2: Export removal (CSV files)
- Clean dependency chain: Feature 2 depends on Feature 1 (sequential execution required)
- Both touch player-data-fetcher module but different files/sections
- No overlapping data structures, config keys, or algorithms

**No conflicts found in:**
- Data Structures ✅
- Interfaces & Dependencies ✅ (clean dependency: Feature 2 → Feature 1)
- File Locations ✅
- Configuration Keys ✅
- Algorithms & Logic ✅
- Testing Assumptions ✅

---

## Resolutions Applied

**No resolutions needed** - zero conflicts found

---

## Final Status

**Conflicts Identified:** 0
**Conflicts Resolved:** 0
**Unresolved Conflicts:** 0

✅ **All features aligned and conflict-free**

**Ready for user sign-off**

---

## Feature Dependencies Diagram

```
Feature 1 (Update Data Models) ──> Feature 2 (Disable CSV Exports)
     │                                   │
     ├─ Migrates drafted → drafted_by   ├─ Removes CSV exports
     ├─ Fixes data model                ├─ Removes export methods
     └─ MUST complete first             └─ Depends on Feature 1
```

**Implementation Order:** Feature 1 FIRST, then Feature 2

**Rationale:** Feature 2 cannot safely execute until Feature 1 fixes the data model. CSV exports would fail with broken data models.

---

## Risk Assessment

**Feature 1 (Update Data Models):**
- **Risk:** LOW
- **Complexity:** LOW
- **Scope:** ~15 items (~20 lines modified, ~18 removed across 6 files)
- **Confidence:** HIGH (investigation complete, no hidden dependencies)

**Feature 2 (Disable CSV Exports):**
- **Risk:** LOW
- **Complexity:** LOW
- **Scope:** ~12 items (~180 lines removed across 4 files)
- **Confidence:** HIGH (investigation complete, only SaveCalculatedPointsManager needs update)

**Combined Epic:**
- **Total Risk:** LOW
- **Total Complexity:** LOW
- **Total Scope:** ~27 items across 9 unique files
- **Estimated Timeline:** Both features are small, can complete in single session per feature

---

## Integration Points Verified

1. **player-data-fetcher module:**
   - Feature 1: Models + conversion logic
   - Feature 2: Export logic
   - ✅ No overlap in specific files/sections

2. **data/ folder:**
   - Feature 1: Changes field names in position JSON
   - Feature 2: Stops creating players.csv and players_projected.csv
   - ✅ Complementary changes

3. **config.py:**
   - Feature 1: Removes PRESERVE_DRAFTED_VALUES, updates EXPORT_COLUMNS
   - Feature 2: Removes PLAYERS_CSV
   - ✅ Different lines, no conflicts

4. **league_helper integration:**
   - Feature 1: Position JSON must have drafted_by field
   - Feature 2: League helper must load from JSON (already does)
   - ✅ Both verified in Stage 2 research

5. **simulation system:**
   - Feature 1: No impact (simulation uses position JSON)
   - Feature 2: No impact (simulation uses sim_data/ historical snapshots, NOT data/players.csv)
   - ✅ Both features safe for simulation

---

**Sanity Check Complete:** 2025-12-30
**Next:** Present plan to user for sign-off
