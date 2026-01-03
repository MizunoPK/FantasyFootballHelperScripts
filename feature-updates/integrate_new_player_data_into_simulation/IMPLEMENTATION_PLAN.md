# Epic Implementation Plan - Ready for Approval

**Epic:** integrate_new_player_data_into_simulation
**Date:** 2026-01-01
**Status:** All features planned, sanity check complete

---

## Feature Summary

### Feature 1: Win Rate Simulation JSON Integration
**Purpose:** Update Win Rate Sim to load player data from 6 position-specific JSON files per week instead of CSV files
**Scope:**
- Modify SimulationManager, SimulatedLeague, DraftHelperTeam, SimulatedOpponent (4 files)
- Add JSON parsing method to extract week-specific data from arrays
- Pre-load and cache all 17 weeks for performance
- Create shared_dir/player_data/ structure

**Dependencies:** None (foundation)
**Risk:** MEDIUM (caching logic complexity)
**Estimate:** ~150 LOC, ~15-20 implementation items

**Key Implementation:**
- `_parse_players_json(week_folder, week_num)` - Extract week N from arrays
- Array indexing: `projected_points[week_num - 1]`
- Shared directory reused across simulation runs

### Feature 2: Accuracy Simulation JSON Integration
**Purpose:** Update Accuracy Sim to load player data from JSON files, verify Week 17/18 logic, ensure DEF/K evaluation is correct
**Scope:**
- Modify AccuracySimulationManager, ParallelAccuracyRunner (2 files)
- Update file copying logic to handle JSON files
- Create temp_dir/player_data/ structure per evaluation
- Verify Week 17/18 and DEF/K handling (validation tasks, not code changes)

**Dependencies:** None (parallel to Feature 1)
**Risk:** LOW (simpler than Feature 1, no caching)
**Estimate:** ~40-50 LOC, ~10-15 implementation items

**Key Implementation:**
- File copying instead of parsing (PlayerManager handles JSON loading)
- Temp directory created per config evaluation
- On-demand loading (no caching needed)

---

## Implementation Order

**Recommended sequence:**

**Option 1: Parallel Implementation (Recommended)**
- Implement Features 1 and 2 simultaneously
- Both are independent (no dependencies)
- Can be developed and tested in parallel
- Reduces total timeline

**Option 2: Sequential Implementation**
- Implement Feature 1 first (Win Rate Sim)
- Then implement Feature 2 (Accuracy Sim)
- Safer approach if wanting to validate approach incrementally

**Recommendation:** Option 1 (Parallel) - Features are truly independent

---

## Dependencies Diagram

```
Feature 1 (Win Rate Sim) ──┐
                           ├──> (No cross-dependencies)
Feature 2 (Accuracy Sim) ──┘
```

**Both features:**
- Read from SAME data source (simulation/sim_data/{year}/weeks/)
- Use SAME file format (6 JSON files per week)
- Operate on DIFFERENT subsystems (Win Rate vs Accuracy)
- NO shared code or interfaces

---

## Risk Assessment

**MEDIUM Risk:**
- Feature 1 (Win Rate Sim) - Caching logic, JSON parsing method, 4 files to modify

**LOW Risk:**
- Feature 2 (Accuracy Sim) - Simpler implementation, file copying only, 2 files to modify

**Mitigation:**
- Both features have complete specs (all questions resolved via codebase investigation)
- Shared patterns identified (player_data/ subfolder, array indexing)
- PlayerManager already handles JSON correctly (no changes needed)
- Intentional differences documented (caching vs on-demand)
- Week 17/18 and DEF/K are validation tasks (tested in QC, no new code)

---

## Sanity Check Results

**Cross-feature comparison complete:**
- ✅ All data structures aligned (same 6 JSON files, same array structure)
- ✅ All interfaces verified (same PlayerManager usage, same dependencies)
- ✅ All file locations consistent (same source location, same file naming)
- ✅ All configuration keys unique (no new keys added by either feature)
- ✅ All algorithms coordinated (intentional differences documented)
- ✅ All testing assumptions clear (separate integration points)

**Conflicts found and resolved:** 0

**Intentional differences (documented):**
1. Feature 1: Pre-loads/caches all 17 weeks (performance for thousands of iterations)
   Feature 2: Loads on-demand per config (simplicity for single evaluations)

2. Feature 1: Needs JSON parsing method to extract week-specific data
   Feature 2: No parsing needed (PlayerManager handles it)

3. Feature 1: Shared directory across simulation
   Feature 2: Temp directory per config evaluation

**All differences justified by different use cases.**

**Ready for implementation:** YES

---

## Shared Patterns (Cross-Feature Alignment)

**Both features use:**
- player_data/ subfolder (required by PlayerManager)
- Array indexing: index 0 = Week 1, index N-1 = Week N
- Same 6 position files: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
- FantasyPlayer.from_json() for type handling (no conversion needed)
- Error handling: return None if week folder missing

**Patterns established in Feature 1 research (reused by Feature 2):**
- PlayerManager.py:327 hardcodes player_data/ path
- json_exporter.py:328 confirms array indexing (bye_idx = week - 1)
- FantasyPlayer.from_json() handles boolean locked and string drafted_by

---

## Next Steps After Approval

1. **Stage 4:** Update epic_smoke_test_plan.md based on this plan
   - Add specific test scenarios for JSON loading
   - Define integration points (Win Rate + Accuracy subsystems)
   - Update success criteria with actual implementation knowledge

2. **Stage 5:** Implement features (choose parallel or sequential)
   - Feature 1: 5a → 5b → 5c → 5d → 5e
   - Feature 2: 5a → 5b → 5c → 5d → 5e

3. **Stage 6:** Epic-level final QC
   - Execute epic_smoke_test_plan.md
   - Validate both simulations work with JSON
   - Verify Week 17/18 and DEF/K handling

4. **Stage 7:** Epic cleanup and completion
   - Unit tests (100% pass)
   - User testing
   - Commit and merge

**Estimated total:** 2 features × Stage 5 workflow = Ready for implementation

---

## Epic Success Criteria

**The epic is successful when:**

1. ✅ Win Rate Simulation loads player data from JSON files (not CSV)
2. ✅ Accuracy Simulation loads player data from JSON files (not CSV)
3. ✅ Both simulations maintain SAME functionality as before (no algorithm changes)
4. ✅ Both simulations correctly handle new field structure (drafted_by string, locked boolean, points arrays)
5. ✅ Week 17 assessment verified working correctly (validation task)
6. ✅ DEF and K positions verified working correctly (validation task)
7. ✅ All unit tests pass (100%)
8. ✅ No regressions in simulation behavior

---

**Date Created:** 2026-01-01
**Status:** Ready for user approval
