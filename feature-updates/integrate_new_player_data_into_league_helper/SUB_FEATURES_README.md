# Sub-Feature Breakdown

This feature has been split into 8 independent sub-features for easier implementation and testing.

## Why Break Down the Feature?

The original feature was becoming unwieldy with:
- 132 implementation items
- 6 large analysis documents
- Multiple independent subsystems affected
- Risk of cascading failures during implementation

## Sub-Features Overview

| Sub-Feature | Items | Dependencies | Risk | Priority |
|-------------|-------|--------------|------|----------|
| [1. Core Data Loading](#1-core-data-loading) | 29 items | None | MEDIUM | HIGH |
| [2. Weekly Data Migration](#2-weekly-data-migration) | 24 items | Sub-feature 1 | MEDIUM | HIGH |
| [3. Locked Field Migration](#3-locked-field-migration) | 21 items | Sub-feature 1 | LOW | MEDIUM |
| [4. File Update Strategy](#4-file-update-strategy) | 22 items | Sub-features 1, 3 | MEDIUM | HIGH |
| [5. ProjectedPointsManager Consolidation](#5-projectedpointsmanager-consolidation) | 10 items | Sub-feature 2 | LOW | MEDIUM |
| [6. TeamDataManager D/ST Migration](#6-teamdatamanager-dst-migration) | 8 items | Sub-feature 2 | MEDIUM | HIGH |
| [7. DraftedRosterManager Consolidation](#7-draftedroster manager-consolidation) | 12 items | Sub-feature 1 | LOW | MEDIUM |
| [8. CSV Deprecation & Cleanup](#8-csv-deprecation--cleanup) | 6 items | All others | LOW | LOW |

**Total: 132 items**

## Implementation Order (Recommended)

### Phase 1: Foundation (Can run in parallel)
1. **Core Data Loading** - Base functionality, no dependencies
2. **Locked Field Migration** - Independent change

### Phase 2: Core Features (Sequential)
3. **Weekly Data Migration** - Depends on Core Data Loading
4. **File Update Strategy** - Depends on Core Data Loading + Locked Field

### Phase 3: Manager Consolidations (Can run in parallel)
5. **ProjectedPointsManager Consolidation** - Depends on Weekly Data Migration
6. **TeamDataManager D/ST Migration** - Depends on Weekly Data Migration
7. **DraftedRosterManager Consolidation** - Depends on Core Data Loading

### Phase 4: Cleanup
8. **CSV Deprecation & Cleanup** - Depends on all others

## Sub-Feature Specifications

Each sub-feature has its own specification file with:
- Objective and scope
- Implementation checklist items
- Dependencies
- Testing requirements
- Success criteria

### 1. Core Data Loading
**File:** `sub_feature_01_core_data_loading_spec.md`

**Objective:** Implement FantasyPlayer.from_json() and PlayerManager JSON loading

**Scope:**
- NEW-1 to NEW-19: Core JSON loading
- NEW-31 to NEW-40: Position-specific stats fields
- NEW-41 to NEW-44: Scope clarifications and validation

**Key Deliverables:**
- FantasyPlayer.from_json() method
- PlayerManager.load_players_from_json() method
- All position-specific stat fields added
- Basic round-trip tests passing

---

### 2. Weekly Data Migration
**File:** `sub_feature_02_weekly_data_migration_spec.md`

**Objective:** Replace week_N_points fields with projected_points/actual_points arrays

**Scope:**
- NEW-22a to NEW-22l: Update all week_N_points usage
- NEW-23 to NEW-30: Method updates and testing
- NEW-25a to NEW-25f: Method analysis decisions (already resolved)

**Key Deliverables:**
- All 17 week_N_points fields removed
- projected_points and actual_points arrays working
- get_weekly_projections() implementing hybrid logic
- All 4 call sites updated

---

### 3. Locked Field Migration
**File:** `sub_feature_03_locked_field_migration_spec.md`

**Objective:** Change locked from int to boolean and standardize to is_locked()

**Scope:**
- NEW-54 to NEW-74: Locked field migration (21 items)
- NEW-49 to NEW-51: Analysis and strategy (resolved)

**Key Deliverables:**
- locked field changed to boolean
- All 14 comparisons updated to use is_locked()
- All 2 assignments updated to use True/False
- Tests passing

---

### 4. File Update Strategy
**File:** `sub_feature_04_file_update_strategy_spec.md`

**Objective:** Migrate update_players_file() to selective JSON updates

**Scope:**
- NEW-75 to NEW-96: update_players_file migration (22 items)
- NEW-45, NEW-52: Migration strategy (resolved)

**Key Deliverables:**
- update_players_file() writes to JSON not CSV
- Selective updates (only drafted_by and locked)
- Atomic write pattern implemented
- Round-trip preservation tests passing

---

### 5. ProjectedPointsManager Consolidation
**File:** `sub_feature_05_projected_points_manager_consolidation_spec.md`

**Objective:** Consolidate ProjectedPointsManager into PlayerManager

**Scope:**
- NEW-100 to NEW-109: Consolidation (10 items)
- NEW-47: Analysis (resolved)

**Key Deliverables:**
- 3 projection methods added to PlayerManager
- player_scoring.py updated
- ProjectedPointsManager deprecated
- Performance deviation calculations verified

---

### 6. TeamDataManager D/ST Migration
**File:** `sub_feature_06_team_data_manager_dst_migration_spec.md`

**Objective:** Migrate TeamDataManager to read from dst_data.json

**Scope:**
- NEW-110 to NEW-117: D/ST migration (8 items)
- NEW-46: Analysis (resolved)

**Key Deliverables:**
- _load_dst_player_data() reads from JSON
- actual_points arrays extracted
- D/ST fantasy rankings working
- Team quality multiplier calculations verified

---

### 7. DraftedRosterManager Consolidation
**File:** `sub_feature_07_drafted_roster_manager_consolidation_spec.md`

**Objective:** Consolidate DraftedRosterManager into PlayerManager

**Scope:**
- NEW-124 to NEW-135: Consolidation (12 items)
- NEW-42: Analysis (resolved)

**Key Deliverables:**
- 3 roster organization methods added to PlayerManager
- TradeSimulatorModeManager updated
- DraftedRosterManager deprecated
- Trade analysis working with new approach

---

### 8. CSV Deprecation & Cleanup
**File:** `sub_feature_08_csv_deprecation_cleanup_spec.md`

**Objective:** Deprecate old CSV files and loading methods

**Scope:**
- NEW-20 to NEW-29: CSV removal (10 items - some merged with other sub-features)

**Key Deliverables:**
- Old CSV loading methods deprecated
- CSV files marked as deprecated
- All modes working with JSON
- Full integration tests passing

---

## Development Workflow

### For Each Sub-Feature:

1. **Read the sub-feature spec** - Understand scope and deliverables
2. **Create TODO file** - Use todo_creation_guide.md (24 iterations)
3. **Interface verification** - Verify all interfaces before coding
4. **Implementation** - Execute TODO tasks with continuous testing
5. **Mini-QC checkpoint** - Verify success criteria
6. **Integration test** - Test with other completed sub-features
7. **Mark complete** - Update this README with ✅

### Completion Tracking:

- [ ] Sub-feature 1: Core Data Loading
- [ ] Sub-feature 2: Weekly Data Migration
- [ ] Sub-feature 3: Locked Field Migration
- [ ] Sub-feature 4: File Update Strategy
- [ ] Sub-feature 5: ProjectedPointsManager Consolidation
- [ ] Sub-feature 6: TeamDataManager D/ST Migration
- [ ] Sub-feature 7: DraftedRosterManager Consolidation
- [ ] Sub-feature 8: CSV Deprecation & Cleanup

### Final Integration:

After ALL sub-features complete:
- Run full test suite (2,200+ tests must pass)
- Run SMOKE TESTING PROTOCOL (3 parts)
- Complete 3 QC rounds
- Move entire folder to done/

---

## Benefits of This Approach

1. **Reduced Complexity** - Each sub-feature is focused and manageable
2. **Parallel Development** - Independent sub-features can be developed simultaneously
3. **Easier Testing** - Smaller scope = easier to verify
4. **Better Error Isolation** - Failures are contained to specific sub-features
5. **Incremental Progress** - Can deploy working sub-features independently
6. **Clearer Dependencies** - Explicit dependency chain prevents conflicts

---

## Reference Documents

All research and analysis documents have been moved to `research/` folder:
- RESEARCH_FINDINGS_2025-12-27.md
- RESEARCH_SUMMARY.md
- VERIFICATION_REPORT_2025-12-27.md
- WEEKLY_DATA_ANALYSIS.md
- PROJECTED_POINTS_MANAGER_ANALYSIS.md
- DRAFTED_ROSTER_MANAGER_ANALYSIS.md

See `research/README.md` for details.
