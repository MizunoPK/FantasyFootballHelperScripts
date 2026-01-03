# Cross-Feature Sanity Check

**Date:** 2026-01-03
**Epic:** integrate_new_player_data_into_simulation
**Features Compared:** 3 features

---

## Comparison Matrix

### Category 1: Data Structures

| Feature | Data Added | Field Names | Data Types | Conflicts? |
|---------|-----------|-------------|------------|------------|
| Feature 01 | None (verifies existing JSON) | N/A | N/A | ❌ None |
| Feature 02 | None (verifies existing JSON) | N/A | N/A | ❌ None |
| Feature 03 | None (testing + docs) | N/A | N/A | ❌ None |

**Check for conflicts:**
- ❌ Duplicate field names? NO - No features add new fields
- ❌ Conflicting types for same field? NO - All features verify existing structure
- ❌ Incompatible data formats? NO - All use same JSON format

**Result:** No data structure conflicts

### Category 2: Interfaces & Dependencies

| Feature | Depends On | Calls Methods | Return Types Expected | Conflicts? |
|---------|-----------|---------------|----------------------|------------|
| Feature 01 | SimulatedLeague._parse_players_json() | Direct JSON parsing | Dict[str, FantasyPlayer] | ❌ None |
| Feature 02 | PlayerManager.load_players_from_json() | PlayerManager delegation | List[FantasyPlayer] | ⚠️ See below |
| Feature 03 | Features 01 AND 02 complete | run_win_rate_simulation.py, run_accuracy_simulation.py | Both complete without errors | ❌ None |

**Check for conflicts:**
- ✅ Feature 01 and 02 use DIFFERENT patterns (by design)
  - Feature 01: Direct JSON parsing in SimulatedLeague
  - Feature 02: PlayerManager delegation (temporary directory pattern)
- ⚠️ **POTENTIAL CONFLICT:** Edge case handling consistency
  - Feature 02 Requirement 7: "Align edge case handling with Win Rate Sim"
  - This addresses potential inconsistencies WITHIN Feature 02 spec
  - NOT a conflict between features (intentional alignment)
- ✅ Feature 03 depends on both Features 01 and 02 being complete
  - Correct dependency mapping
  - Sequential implementation required

**Result:** No interface conflicts (different patterns are intentional)

### Category 3: File Locations & Naming

| Feature | Creates Files | File Locations | Naming Conventions | Conflicts? |
|---------|--------------|----------------|-------------------|------------|
| Feature 01 | No new files (deletes _parse_players_csv) | simulation/win_rate/*.py | N/A | ❌ None |
| Feature 02 | No new files (updates existing) | simulation/accuracy/*.py | N/A | ❌ None |
| Feature 03 | No new files (updates docs) | simulation/README.md + docstrings | N/A | ❌ None |

**Check for conflicts:**
- ❌ File naming conflicts? NO - No new files created
- ❌ Directory conflicts? NO - Features work in separate directories:
  - Feature 01: simulation/win_rate/
  - Feature 02: simulation/accuracy/
  - Feature 03: simulation/ (README and docstrings across both)
- ✅ Feature 03 updates documentation in BOTH directories (by design)

**Result:** No file location conflicts

### Category 4: Configuration Keys

| Feature | Config Keys Added | Config File | Key Conflicts? | Conflicts? |
|---------|------------------|-------------|----------------|------------|
| Feature 01 | None (verification only) | N/A | N/A | ❌ None |
| Feature 02 | None (verification only) | N/A | N/A | ❌ None |
| Feature 03 | None (testing + docs) | N/A | N/A | ❌ None |

**Check for conflicts:**
- ❌ Configuration key conflicts? NO - No features add new config keys
- ✅ All features verify existing configuration

**Result:** No configuration conflicts

### Category 5: Algorithms & Logic

| Feature | Algorithm Type | Multiplier/Score Impact | Order Dependencies | Conflicts? |
|---------|---------------|------------------------|-------------------|------------|
| Feature 01 | Direct JSON parsing (Win Rate Sim) | Week_N+1 fix, array indexing, edge cases | None | ❌ None |
| Feature 02 | PlayerManager delegation (Accuracy Sim) | Week_N+1 fix, edge case alignment | Feature 01 (align with edge cases) | ✅ Aligned |
| Feature 03 | End-to-end testing (both sims) | Tests both patterns work | Features 01, 02 (must complete first) | ❌ None |

**Check for conflicts:**
- ✅ Feature 02 Requirement 7 explicitly aligns edge cases with Feature 01:
  - Missing week_N+1 folder: Both use "fallback to projected data"
  - Array index out of bounds: Both use "default to 0.0"
- ✅ Both features implement Week_N+1 logic correctly
  - Feature 01: _preload_week_data() with week_num_for_actual parameter
  - Feature 02: _load_season_data() returns (week_N, week_N+1)
- ✅ Feature 03 tests BOTH patterns (no conflict, just verification)

**Result:** No algorithm conflicts (Feature 02 explicitly aligns with Feature 01)

### Category 6: Testing Assumptions

| Feature | Test Data Needs | Mock Dependencies | Integration Points | Conflicts? |
|---------|----------------|-------------------|-------------------|------------|
| Feature 01 | JSON test data (weeks 1, 10, 17) | None (uses real data) | None (self-contained) | ❌ None |
| Feature 02 | JSON test data (weeks 1, 10, 17) | None (uses real PlayerManager) | PlayerManager (league_helper) | ❌ None |
| Feature 03 | Both sims working + JSON data | Features 01 & 02 complete | run_win_rate_sim + run_accuracy_sim | ❌ None |

**Check for conflicts:**
- ✅ All features use REAL data (no mocking conflicts)
  - Feature 01: Uses real JSON files from week folders
  - Feature 02: Uses real PlayerManager with real JSON files
  - Feature 03: Uses real simulations (end-to-end testing)
- ✅ Test data requirements align:
  - All features test weeks 1, 10, and 17 (consistent coverage)
  - Feature 03 depends on Features 01 & 02 being complete (correct dependency)
- ✅ Integration points well-defined:
  - Feature 01: Self-contained (direct parsing)
  - Feature 02: Integrates with PlayerManager (already migrated)
  - Feature 03: Integrates with both simulations

**Result:** No testing conflicts

---

## Systematic Comparison Complete

**Categories Compared:** 6
**Features Compared:** 3
**Pairwise Comparisons:** 3 features across 6 categories

---

## Conflicts Identified

**Total Conflicts Found:** 0

**Analysis:**
- ❌ Data Structures: No conflicts (no new fields added by any feature)
- ❌ Interfaces & Dependencies: No conflicts (different patterns by design; Feature 02 aligns with Feature 01)
- ❌ File Locations: No conflicts (features work in separate directories)
- ❌ Configuration Keys: No conflicts (no new config keys added)
- ❌ Algorithms & Logic: No conflicts (Feature 02 explicitly aligns edge cases with Feature 01)
- ❌ Testing Assumptions: No conflicts (all use real data; correct dependencies)

**Key Observations:**
1. **Feature 02 Requirement 7** proactively aligns edge case handling with Feature 01
   - This is NOT a conflict - it's intentional alignment built into the spec
   - Prevents future inconsistencies between simulations

2. **Different architectural patterns** are intentional:
   - Feature 01: Direct JSON parsing (Win Rate Sim)
   - Feature 02: PlayerManager delegation (Accuracy Sim)
   - Both patterns are correct for their respective simulations

3. **Clear dependency chain:**
   - Features 01 and 02 are independent (can be implemented in parallel)
   - Feature 03 depends on Features 01 AND 02 (sequential after first two)

---

## Resolutions Applied

**Total Resolutions Needed:** 0

**Analysis:**
Since no conflicts were identified during systematic comparison, no resolutions are required.

**Verification:**
- ✅ All features have aligned specifications
- ✅ No spec updates needed
- ✅ No new conflicts introduced
- ✅ Feature dependencies correctly identified
- ✅ Implementation order clear (Features 01, 02 parallel → Feature 03 sequential)

**Status:** All features are conflict-free and ready for implementation

---

## Final Status

**Conflicts Identified:** 0
**Conflicts Resolved:** 0
**Unresolved Conflicts:** 0

✅ **All features aligned and conflict-free**

**Ready for user sign-off**
