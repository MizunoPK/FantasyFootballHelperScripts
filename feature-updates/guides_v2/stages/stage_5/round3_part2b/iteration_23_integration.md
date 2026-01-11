# Iteration 23: Integration Gap Check

**Part of:** STAGE 5ac Part 2b - Round 3 Gate 3
**Purpose:** Verify ALL implementation tasks have integration points (no orphan code)
**Prerequisites:** Round 3 Part 2a started, iterations 17-22 complete
**Time Estimate:** 15-20 minutes

---

## Purpose

**Integration Gap Check** prevents "orphan code" - code that gets implemented but never called/used.

**Historical Context:**
- Feature 01 implemented `_load_json_player_data()` but no caller existed
- Code written, tested, but never executed in actual feature flow
- Discovered during Stage 5c smoke testing
- Required emergency implementation of caller + integration tests

**This iteration prevents implementing code that won't be used.**

---

## Process

### STEP 1: List all implementation methods/functions from implementation_plan.md

```markdown
## Implementation Methods Inventory

**From implementation_plan.md Implementation Tasks section:**

### Methods to implement:
1. `_load_json_player_data()` - Load JSON files from sim_data folders
2. `_build_week_folder_path()` - Construct week_N folder paths
3. `_parse_player_json()` - Parse player JSON structure
4. `_calculate_win_rate()` - Calculate win rate from simulation results
5. `_aggregate_weekly_scores()` - Aggregate scores across weeks
6. `_generate_summary_report()` - Generate final summary
7. `_validate_json_schema()` - Validate JSON structure
8. `_handle_missing_weeks()` - Handle missing week data
9. `_load_projected_points()` - Load projected points from week_N
10. `_load_actual_points()` - Load actual points from week_N+1
11. `_merge_projected_actual()` - Merge projected and actual data
12. `run_simulation()` - Main entry point (UPDATE existing)

**Total methods:** 12 (11 new + 1 update)

---
```

---

### STEP 2: For each method, identify caller

```markdown
## Integration Verification - Method Callers

### Method 1: `_load_json_player_data()`
**Caller:** `run_simulation()` (line 47 in implementation_plan.md)
**Call site:** "Phase 1 - Data Loading" task
**Evidence:** implementation_plan.md Task 1.3 shows `run_simulation()` calls `_load_json_player_data()`
**Status:** ✅ HAS CALLER

---

### Method 2: `_build_week_folder_path()`
**Caller:** `_load_json_player_data()` (Task 1.1)
**Call site:** Inside data loading loop
**Evidence:** implementation_plan.md Task 1.1 shows path construction calls this helper
**Status:** ✅ HAS CALLER

---

### Method 3: `_parse_player_json()`
**Caller:** `_load_json_player_data()` (Task 1.2)
**Call site:** After reading JSON file
**Evidence:** implementation_plan.md Task 1.2 shows JSON parsing calls this method
**Status:** ✅ HAS CALLER

---

### Method 4: `_calculate_win_rate()`
**Caller:** `run_simulation()` (Phase 3 - Win Rate Calculation)
**Call site:** After data aggregation
**Evidence:** implementation_plan.md Task 3.1 shows calculation phase calls this
**Status:** ✅ HAS CALLER

---

### Method 5: `_aggregate_weekly_scores()`
**Caller:** `_calculate_win_rate()` (internal step)
**Call site:** Before win rate computation
**Evidence:** implementation_plan.md Task 2.2 shows aggregation happens before calculation
**Status:** ✅ HAS CALLER

---

### Method 6: `_generate_summary_report()`
**Caller:** `run_simulation()` (Phase 5 - Reporting)
**Call site:** Final phase
**Evidence:** implementation_plan.md Task 5.1 shows report generation at end
**Status:** ✅ HAS CALLER

---

### Method 7: `_validate_json_schema()`
**Caller:** `_parse_player_json()` (Task 1.2)
**Call site:** Before parsing JSON
**Evidence:** implementation_plan.md Task 1.2.1 shows validation before parsing
**Status:** ✅ HAS CALLER

---

### Method 8: `_handle_missing_weeks()`
**Caller:** `_load_json_player_data()` (error handling)
**Call site:** When week file not found
**Evidence:** implementation_plan.md Task 1.4 shows error handling for missing weeks
**Status:** ✅ HAS CALLER

---

### Method 9: `_load_projected_points()`
**Caller:** `_load_json_player_data()` (Task 1.5)
**Call site:** Week N folder loading
**Evidence:** implementation_plan.md Task 1.5 shows week_N loading for projected
**Status:** ✅ HAS CALLER

---

### Method 10: `_load_actual_points()`
**Caller:** `_load_json_player_data()` (Task 1.6)
**Call site:** Week N+1 folder loading
**Evidence:** implementation_plan.md Task 1.6 shows week_N+1 loading for actual
**Status:** ✅ HAS CALLER

---

### Method 11: `_merge_projected_actual()`
**Caller:** `_load_json_player_data()` (Task 1.7)
**Call site:** After loading both projected and actual
**Evidence:** implementation_plan.md Task 1.7 shows merging step
**Status:** ✅ HAS CALLER

---

### Method 12: `run_simulation()` (UPDATE)
**Caller:** External - User calls this from CLI/script
**Call site:** Entry point
**Evidence:** spec.md shows this is main public method
**Status:** ✅ HAS CALLER (external)

---

## Summary: Integration Verification

**Total methods:** 12
**Methods with callers:** 12 ✅
**Orphan methods (no caller):** 0 ✅

**Status:** ✅ ALL METHODS HAVE CALLERS

---
```

---

### STEP 3: Identify orphan code (no caller)

**If ANY method has "❌ NO CALLER":**

```markdown
## ⚠️ ORPHAN CODE DETECTED

### Orphan Method 1: `_example_method()`
**Status:** ❌ NO CALLER
**Reason:** No implementation task calls this method
**Impact:** Code will be implemented but never executed

**Resolution options:**
1. Remove method from implementation plan (not needed)
2. Add caller to appropriate task
3. Ask user if method is needed

**Recommended:** Remove from plan (orphan code)

---
```

**If no orphan code:**

```markdown
## ✅ No Orphan Code Detected

**All 12 methods have identified callers.**

**Integration verification complete.**

---
```

---

### STEP 4: Verify integration flows end-to-end

**Trace execution flow from entry point to exit:**

```markdown
## End-to-End Integration Flow

**Entry Point:** `run_simulation()` (external caller)

**Execution Flow:**

1. **Phase 1 - Data Loading:**
   - `run_simulation()` calls `_load_json_player_data()`
   - `_load_json_player_data()` calls:
     - `_build_week_folder_path()` → Construct paths
     - `_load_projected_points()` → Load week_N data
     - `_load_actual_points()` → Load week_N+1 data
     - `_parse_player_json()` → Parse JSON
       - `_validate_json_schema()` → Validate structure
     - `_merge_projected_actual()` → Merge data
     - `_handle_missing_weeks()` → Handle errors

2. **Phase 2 - Data Aggregation:**
   - `run_simulation()` calls `_aggregate_weekly_scores()`

3. **Phase 3 - Win Rate Calculation:**
   - `run_simulation()` calls `_calculate_win_rate()`

4. **Phase 4 - Validation:**
   - (Built into previous phases)

5. **Phase 5 - Reporting:**
   - `run_simulation()` calls `_generate_summary_report()`

**Exit Point:** Return summary report to caller

**Status:** ✅ COMPLETE FLOW - Entry to exit traced

---
```

---

### STEP 5: Document gaps and recommendations

```markdown
## Integration Gap Analysis

**Gaps Found:** 0 ✅

**Recommendations:**
1. All methods have callers - no orphan code
2. Execution flow is complete from entry to exit
3. Error handling integrated into flow
4. No missing integration points

**Next Step:** Proceed to Iteration 23a (Pre-Implementation Spec Audit)

---
```

**If gaps found, document:**

```markdown
## Integration Gap Analysis

**Gaps Found:** {N}

### Gap 1: Missing caller for `_example_method()`
**Problem:** Method planned but no caller exists
**Impact:** Code will be orphaned
**Recommendation:** Remove method OR add caller in Task X.Y
**User decision needed:** Should we keep this method?

---

### Gap 2: Incomplete flow from Phase 2 to Phase 3
**Problem:** No method connects aggregation to calculation
**Impact:** Data aggregation results not passed to win rate calculation
**Recommendation:** Add connector method `_prepare_calculation_data()` in Task 2.3
**User decision needed:** Confirm this is needed

---

**STOP - Resolve gaps before proceeding to Iteration 23a**

---
```

---

### STEP 6: Update implementation_plan.md with integration verification

**Add to implementation_plan.md:**

```markdown
---

## Integration Verification (Iteration 23)

**Date:** {YYYY-MM-DD}
**Status:** ✅ PASSED

**Methods verified:** 12/12
**Methods with callers:** 12
**Orphan methods:** 0

**Integration Flow:**
- Entry point: `run_simulation()` (external)
- Exit point: Return summary report
- Flow completeness: 100%

**Gaps found:** 0

**RESULT:** ✅ All implementation tasks are integrated, no orphan code

---
```

---

## Completion Criteria

**Iteration 23 is COMPLETE when ALL of these are true:**

- [ ] All methods/functions listed from implementation_plan.md
- [ ] Every method has identified caller
- [ ] Orphan code identified (if any)
- [ ] End-to-end flow traced
- [ ] Gaps documented (if any)
- [ ] implementation_plan.md updated with verification results
- [ ] If gaps found → User decision obtained before proceeding

---

## Common Mistakes to Avoid

### ❌ MISTAKE: "I'll assume all methods are called"

**Why this is wrong:**
- Assumptions miss orphan code
- Orphan code discovered during smoke testing = emergency fixes

**What to do instead:**
- ✅ Explicitly verify EACH method has caller
- ✅ Trace caller references from implementation_plan.md
- ✅ Document evidence for each caller

---

### ❌ MISTAKE: "Method is in plan, so it must be needed"

**Why this is wrong:**
- Methods can be planned but not integrated
- "Planned" ≠ "Called"

**What to do instead:**
- ✅ Verify caller exists in implementation tasks
- ✅ If no caller found, recommend removal or add caller

---

## Next Step

**After Iteration 23 completes:**

Proceed to **Iteration 23a (Pre-Implementation Spec Audit - Gate 2)** in gate_23a_spec_audit.md

**📖 READ:** `stages/stage_5/round3_part2b/gate_23a_spec_audit.md`

---

**END OF ITERATION 23 GUIDE**
