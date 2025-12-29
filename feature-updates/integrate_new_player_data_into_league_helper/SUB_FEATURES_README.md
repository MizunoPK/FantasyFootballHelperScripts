# Sub-Feature Breakdown

This feature has been split into 8 independent sub-features for easier implementation and testing, plus 1 bug fix sub-feature discovered during verification.

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
| **[9. drafted Field Deprecation (BUG FIX)](#9-drafted-field-deprecation-bug-fix)** | **TBD** | **Sub-feature 7** | **MEDIUM** | **HIGH** |

**Total: 132+ items** (Sub-feature 9 to be scoped during planning)

## Implementation Order (SEQUENTIAL - NO PARALLELIZATION)

**CRITICAL:** Sub-features MUST be implemented sequentially. Each sub-feature completes FULLY (TODO → Implementation → QC → Commit) before starting the next.

**Phases below show logical groupings for understanding dependencies. NOT for parallel execution.**

### Phase 1: Foundation
1. **Core Data Loading** - Base functionality, no dependencies
2. **Locked Field Migration** - Independent change (but sequential after 1)

### Phase 2: Core Features
3. **Weekly Data Migration** - Depends on Core Data Loading
4. **File Update Strategy** - Depends on Core Data Loading + Locked Field

### Phase 3: Manager Consolidations
5. **ProjectedPointsManager Consolidation** - Depends on Weekly Data Migration
6. **TeamDataManager D/ST Migration** - Depends on Weekly Data Migration
7. **DraftedRosterManager Consolidation** - Depends on Core Data Loading

### Phase 4: Bug Fixes & Cleanup
9. **drafted Field Deprecation (BUG FIX)** - Depends on DraftedRosterManager Consolidation
8. **CSV Deprecation & Cleanup** - Depends on all others

**Execution:** 1 → 2 → 3 → 4 → 5 → 6 → 7 → **9 (BUG FIX)** → 8 (one at a time)

**⚠️ IMPORTANT:** Sub-feature 9 must be completed AFTER sub-feature 7 (which adds drafted_by field) and BEFORE sub-feature 8 (CSV deprecation) to avoid updating deprecated code.

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

### 9. drafted Field Deprecation (BUG FIX)
**File:** `drafted_field_deprecation_bugfix_notes.txt` (will create spec during planning)

**Objective:** Phase out `drafted` int field in favor of `drafted_by` string field with helper methods

**Background:**
During Sub-feature 7 TODO verification, discovered that `drafted_by` field was missing from FantasyPlayer. Added as quick fix, but now we have TWO fields tracking the same information:
- `drafted: int` (0=free agent, 1=opponent, 2=our team) - LEGACY
- `drafted_by: str` (""=free agent, "Team Name"=opponent, "Sea Sharp"=our team) - CORRECT

Original notes explicitly stated to use `drafted_by`, not maintain both fields.

**Scope (TBD during planning):**
- Add 3 helper methods: `is_free_agent()`, `is_drafted_by_opponent()`, `is_rostered()`
- Replace all `player.drafted` comparisons with helper method calls
- Replace all `player.drafted` assignments with `drafted_by` string assignments
- Deprecate `drafted` field (keep for backward compatibility via property)
- Update `from_json()` and `from_dict()` to derive `drafted` from `drafted_by`
- Full test suite verification

**Key Deliverables:**
- Single source of truth (`drafted_by` string)
- Readable API (helper methods instead of magic numbers)
- No data loss (team names preserved)
- Backward compatibility (drafted as derived property)
- All tests passing (100% required)

**Priority:** HIGH - Prevents accumulating technical debt before CSV deprecation

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

**Planning Phase (Deep Dive - Phases 1-4):**
- [x] Sub-feature 1: Core Data Loading - Deep Dive ✅ (2025-12-28)
- [x] Sub-feature 2: Weekly Data Migration - Deep Dive ✅ (2025-12-28)
- [x] Sub-feature 3: Locked Field Migration - Deep Dive ✅ (2025-12-28)
- [x] Sub-feature 4: File Update Strategy - Deep Dive ✅ (2025-12-28)
- [x] Sub-feature 5: ProjectedPointsManager Consolidation - Deep Dive ✅ (2025-12-28)
- [x] Sub-feature 6: TeamDataManager D/ST Migration - Deep Dive ✅ (2025-12-28)
- [x] Sub-feature 7: DraftedRosterManager Consolidation - Deep Dive ✅ (2025-12-28)
- [x] Sub-feature 8: CSV Deprecation & Cleanup - Deep Dive ✅ (2025-12-28)
- [ ] **Sub-feature 9: drafted Field Deprecation (BUG FIX)** - Pending (after sub-features 5-8 complete)

**Implementation Phase (TODO Creation → QC):**
- [ ] Sub-feature 1: Core Data Loading - Implementation
- [ ] Sub-feature 2: Weekly Data Migration - Implementation
- [ ] Sub-feature 3: Locked Field Migration - Implementation
- [ ] Sub-feature 4: File Update Strategy - Implementation
- [ ] Sub-feature 5: ProjectedPointsManager Consolidation - Implementation
- [ ] Sub-feature 6: TeamDataManager D/ST Migration - Implementation
- [ ] Sub-feature 7: DraftedRosterManager Consolidation - Implementation
- [ ] **Sub-feature 9: drafted Field Deprecation (BUG FIX)** - Implementation
- [ ] Sub-feature 8: CSV Deprecation & Cleanup - Implementation

---

## Sub-Feature Completion Status

| Sub-Feature | Planning | TODO | Implementation | QC | Status |
|-------------|----------|------|----------------|----|---------|
| 1. Core Data Loading | ✅ | ✅ | ✅ | ✅ (3/3) | **COMPLETE** |
| 2. Weekly Data Migration | ✅ | ✅ | ✅ | ✅ (3/3) | **COMPLETE** |
| 3. Locked Field Migration | ✅ | ✅ | ✅ | ✅ (3/3) | **COMPLETE** |
| 4. File Update Strategy | ✅ | ✅ | ✅ | ✅ (3/3) | **COMPLETE** |
| 5. ProjectedPointsManager Consolidation | ✅ | ✅ | ✅ | ✅ (3/3) | **COMPLETE** |
| 6. TeamDataManager D/ST Migration | ✅ | ✅ | ✅ | ✅ (3/3) | **COMPLETE** |
| 7. DraftedRosterManager Consolidation | ✅ | ⏸️ (1/24) | ⏸️  | ⏸️  | **PAUSED (Iter 1)** |
| **9. drafted Field Deprecation (BUG FIX)** | ⏸️  | ⏸️  | ⏸️  | ⏸️  | **NEXT (BUG FIX)** |
| 8. CSV Deprecation & Cleanup | ✅ | ⏸️  | ⏸️  | ⏸️  | Pending |

**Progress:** 6/9 sub-features complete (67%)

**Last Updated:** 2025-12-29

**Current Sub-Feature:** Sub-Feature 9: drafted Field Deprecation (BUG FIX) - **READY FOR IMPLEMENTATION**
- ✅ Planning complete (Deep Dive phases 1-4 complete)
- ✅ TODO creation complete (ALL 24 verification iterations PASSED)
- ✅ Questions file: NO questions needed (all 3 decisions resolved during planning)
- ✅ Test baseline: 2415/2415 (100%)
- ✅ Confidence level: HIGH across all areas
- ✅ Scope: 28 occurrences across 8 files (simulation out of scope)
- 🎯 Next: Execute implementation_execution_guide.md

**Remaining Sub-Features:**
- Sub-feature 7: DraftedRosterManager Consolidation - **PAUSED** (resume after Sub-feature 9)
- Sub-feature 9: drafted Field Deprecation (BUG FIX) - **NEXT**
- Sub-feature 8: CSV Deprecation & Cleanup - **PENDING** (after Sub-feature 9)

---

## Ready for Implementation

**Status:** ✅ Planning complete (2025-12-28) - Sub-features 1-2 COMPLETE

**Implementation Order:**
1. **Sub-feature 1: Core Data Loading** (no dependencies) - ✅ **COMPLETE**
2. **Sub-feature 2: Weekly Data Migration** (depends on 1) - ✅ **COMPLETE**
3. **Sub-feature 3: Locked Field Migration** (depends on 1) - ⏸️ **NEXT**
4. **Sub-feature 7: DraftedRosterManager Consolidation** (depends on 1)
5. **Sub-feature 4: File Update Strategy** (depends on 1, 3)
6. **Sub-feature 5: ProjectedPointsManager Consolidation** (depends on 2)
7. **Sub-feature 6: TeamDataManager D/ST Migration** (depends on 2)
8. **Sub-feature 8: CSV Deprecation & Cleanup** (depends on ALL 1-7)

**Process:** For EACH sub-feature sequentially:
1. Execute `todo_creation_guide.md` (FULL 24 iterations)
   - Round 1: Iterations 1-7 (+ iteration 4a)
   - Round 2: Iterations 8-16
   - Round 3: Iterations 17-24 (+ iteration 23a)
   - Creates `sub_feature_{N}_{name}_todo.md`
   - Creates `sub_feature_{N}_{name}_questions.md` (if needed)
2. Execute `implementation_execution_guide.md` (FULL process)
   - Interface verification (MANDATORY)
   - Continuous spec compliance checking
   - Mini-QC checkpoints after each component
   - Creates `sub_feature_{N}_{name}_implementation_checklist.md`
   - Creates `sub_feature_{N}_{name}_code_changes.md`
3. Execute `post_implementation_guide.md` (FULL QC + smoke testing)
   - Smoke testing protocol (3 parts)
   - 3 QC rounds (no exceptions)
   - Update lessons learned
4. Commit changes (one commit per sub-feature)
5. Mark complete in this file
6. Move to next sub-feature

**NO SKIPPING:** All quality gates apply to each sub-feature.

**Cross-Sub-Feature Alignment:** ✅ Verified (Phase 6 complete)
- 1 conflict resolved (locked field timing)
- All interface contracts aligned
- Dependency chain validated (no circular dependencies)

---

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
