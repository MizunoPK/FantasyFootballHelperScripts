# Guide Update Recommendations - Issue #001

**Epic:** KAI-5-add_k_dst_ranking_metrics_support
**Issue:** Incomplete Simulation Results - Missing Ranking Metrics and Metadata
**Root Cause Category:** Backward Compatibility Oversight
**Date:** 2026-01-09

---

## Summary

This document contains concrete guide updates to prevent similar bugs from occurring in future epics. All recommendations are based on systematic analysis of why Issue #001 got through our development process.

**Primary Gap:** Backward compatibility with existing data was not considered during research, spec design, or testing phases.

**Impact:** Bug discovered in Stage 6c (User Testing) that could have been prevented during Stage 5a (Research) or Stage 5ca (Smoke Testing).

---

## Guide Update 1: Stage 5a Round 1 - Add Backward Compatibility Research

**File:** `feature-updates/guides_v2/stages/stage_5/round1_todo_creation.md`

**Location:** Add new iteration after Iteration 7 (Testing Requirements)

**Current State:** Round 1 has 7 iterations, none explicitly prompt for backward compatibility analysis

**Recommended Change:**

### Add New Iteration 7a: Backward Compatibility Analysis

**Insert after line ~280 (after Iteration 7: Testing Requirements Analysis):**

```markdown
### Iteration 7a: Backward Compatibility Analysis (NEW - MANDATORY)

**Objective:** Identify how this feature interacts with existing data, files, and configurations created by older versions of the code.

**Why This Matters:** New features often modify data structures or file formats. If the system can resume/load old data, the new code must handle old formats gracefully. This iteration prevents bugs caused by old data polluting new calculations.

**Research Questions:**

1. **Data Persistence:**
   - Does this feature modify any data structures that are saved to files?
   - Can the system resume/load from files created before this epic?
   - What file formats are involved? (JSON, CSV, pickled objects, etc.)

2. **Old Data Handling:**
   - What happens if new code loads old files missing new fields?
   - Will old data be used in comparisons/calculations with new data?
   - Are there fallback mechanisms that might hide incompatibilities?

3. **Migration Strategy:**
   - Do old files need to be migrated to new format?
   - Should old files be ignored/invalidated?
   - Is there a version marker in saved files?

4. **Resume Scenarios:**
   - Can users resume operations from intermediate states?
   - What happens if intermediate files are from older code version?
   - Will the system detect and handle version mismatches?

**Action Items:**

1. **Search for file I/O operations:**
   - Look for save/load methods in affected modules
   - Check JSON serialization/deserialization
   - Identify resume/checkpoint logic

2. **Analyze data structures:**
   - List all fields added/removed/modified
   - Check if structures have version markers
   - Verify default values for missing fields

3. **Document findings in questions.md:**
   ```markdown
   ## Backward Compatibility Analysis (Iteration 7a)

   **Files that persist data:**
   - [List files and formats]

   **New fields added:**
   - [List new fields with types]

   **Resume/load scenarios:**
   - [Describe scenarios where old data might be loaded]

   **Compatibility strategy:**
   - [ ] Option 1: Migrate old files on load
   - [ ] Option 2: Invalidate old files (require fresh run)
   - [ ] Option 3: Handle missing fields with defaults
   - [ ] Option 4: No old files exist / not applicable

   **Rationale:** [Explain chosen strategy]
   ```

4. **Add test scenarios to todo.md:**
   - If resume/load possible: Add test "Resume from file created before this epic"
   - If migration needed: Add test "Migrate old file format to new format"
   - If validation needed: Add test "Reject incompatible old files with clear error"

**Success Criteria:**

- ✅ All file I/O operations identified and analyzed
- ✅ Compatibility strategy documented and justified
- ✅ Resume/load scenarios covered in test plan
- ✅ Migration or validation logic added to todo.md (if needed)

**Time Estimate:** 10-15 minutes (prevents hours of debugging)

**Historical Evidence:** Issue #001 (KAI-5) discovered in user testing could have been prevented by this iteration. Resume logic loaded old files without ranking_metrics, polluting best_configs with invalid data.
```

**Rationale:**
- Issue #001 occurred because old intermediate files were loaded and polluted best_configs
- Research phase didn't consider "what happens if we resume from old files?"
- This iteration explicitly prompts for backward compatibility analysis
- 10-15 minutes of research prevents hours of debugging in later stages

---

## Guide Update 2: Stage 5a Round 2 - Add Resume Testing Requirement

**File:** `feature-updates/guides_v2/stages/stage_5/round2_todo_creation.md`

**Location:** Iteration 9 (Test Coverage Deep Dive)

**Current State:** Iteration 9 focuses on test coverage metrics but doesn't explicitly require resume scenario testing

**Recommended Change:**

**Insert in Iteration 9: Test Coverage Deep Dive (after line ~100, in test scenario checklist):**

```markdown
### Resume/Persistence Testing (if applicable)

**Trigger:** Feature modifies persisted data OR system supports resume/checkpoint

**Required Test Scenarios:**

1. **Resume from old data:**
   - Create intermediate files with OLD data format (missing new fields)
   - Run new code that loads these files
   - Verify: Old data doesn't pollute new calculations
   - Verify: System handles missing fields gracefully (migrate, ignore, or error)

2. **Resume from partial state:**
   - Interrupt operation mid-execution
   - Verify: Can resume without data corruption
   - Verify: Resume produces same result as fresh run

3. **Version mismatch detection:**
   - If files have version markers, test version mismatch handling
   - Verify: Clear error message when incompatible version detected

**Add to todo.md:**
```markdown
## Backward Compatibility Tests

**Scenario:** Resume from intermediate files created before this epic
- [ ] Create old-format test files (manually or with old code version)
- [ ] Load with new code
- [ ] Verify old data doesn't corrupt new results
- [ ] Verify appropriate handling (migrate/ignore/error)
```

**Coverage Target:** If resume possible → 100% of load paths tested with old data

**Why This Matters:** Resume bugs are hard to catch with fresh-run tests. Old data can silently corrupt new calculations if not explicitly tested.
```

**Rationale:**
- Smoke tests and QC rounds typically use fresh runs
- Resume scenarios were completely untested in KAI-5
- This makes resume testing an explicit requirement when applicable

---

## Guide Update 3: Stage 5a Round 3 Iteration 23a - Challenge Design Decisions

**File:** `feature-updates/guides_v2/stages/stage_5/round3_todo_creation.md`

**Location:** Iteration 23a (MANDATORY GATE - Pre-Implementation Spec Audit)

**Current State:** Iteration 23a has comprehensive spec review checklist but doesn't explicitly prompt for challenging design decisions

**Recommended Change:**

**Add new section to Iteration 23a checklist (after "Code Quality Implications" section, around line ~220):**

```markdown
### Design Decision Scrutiny

**Objective:** Challenge all "for backward compatibility" or "fallback" design decisions

**Checklist:**

- [ ] **Identify all fallback mechanisms:**
  - Search spec.md for: "fallback", "backward compatibility", "default to", "if not available"
  - List all conditional logic that handles missing/incomplete data

- [ ] **For each fallback, ask:**
  - **Why is fallback needed?** (Old data? Partial data? Error recovery?)
  - **What happens when fallback is used?** (Degraded accuracy? Silent failure?)
  - **Can old and new data be compared?** (If yes, what's the comparison logic?)
  - **Could fallback hide bugs?** (Old data appearing valid when it's not)

- [ ] **Challenge the design:**
  - **Is fallback actually safer than failing fast?**
  - **Should incompatible data be rejected instead?**
  - **Does fallback create mixed-mode comparison problems?**

- [ ] **Document in spec.md:**
  ```markdown
  ## Design Decision: [Fallback Name]

  **Rationale:** [Why fallback is needed]
  **Behavior:** [What happens when triggered]
  **Risks:** [Potential issues with this design]
  **Mitigation:** [How risks are addressed]
  **Alternative Considered:** [Why we didn't fail fast / reject old data]
  ```

**Red Flags (require extra scrutiny):**

- ❌ Fallback allows comparing data WITH new metrics vs WITHOUT new metrics
- ❌ "Backward compatibility" mentioned but no version detection logic
- ❌ Missing fields handled silently (no logging/warning)
- ❌ Resume logic populates production data structures with old data

**Example from KAI-5 Issue #001:**

**Bad Design (caused bug):**
```python
# Fallback to MAE for backward compatibility
if self.overall_metrics and other.overall_metrics:
    return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy
return self.mae < other.mae
```

**Problem:** Old configs (without metrics) could beat new configs (with metrics) in MAE comparison, even if new config had better pairwise_accuracy.

**Better Design:**
```python
# Reject configs without metrics as invalid
if not self.overall_metrics:
    return False  # Cannot be "best"
if not other.overall_metrics:
    return True   # Replace invalid with valid
return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy
```

**Success Criteria:**

- ✅ All fallback mechanisms identified and documented
- ✅ Each fallback has documented rationale, risks, and mitigation
- ✅ No fallback allows mixed-mode comparisons (old vs new data)
- ✅ Incompatible data is either migrated, rejected, or isolated (not mixed)
```

**Rationale:**
- Issue #001 had MAE fallback "for backward compatibility" that was never questioned
- The fallback allowed invalid comparisons (configs with metrics vs without)
- Spec review should have caught this design flaw
- This adds explicit scrutiny to fallback/compatibility design decisions

---

## Guide Update 4: Stage 5c Smoke Testing - Add Resume Scenario

**File:** `feature-updates/guides_v2/stages/stage_5/smoke_testing.md`

**Location:** Part 3: E2E/Integration Tests

**Current State:** Smoke testing has import, entry point, and E2E tests but doesn't mention resume scenarios

**Recommended Change:**

**Add new section after E2E tests (around line ~180):**

```markdown
### Resume/Persistence Testing (if applicable)

**When to run:** Feature modifies persisted data OR system supports resume/checkpoint

**Test Procedure:**

1. **Prepare old data (if backward compatibility required):**
   ```bash
   # Option 1: Use old code version to generate files
   git checkout <previous-commit>
   <run command to generate intermediate files>
   git checkout <current-branch>

   # Option 2: Manually create old-format files
   # Copy old files from previous runs to test directory
   ```

2. **Run new code with old data:**
   ```bash
   <run command that loads/resumes from old files>
   ```

3. **Verify results:**
   - [ ] Old data handled appropriately (migrated/ignored/rejected)
   - [ ] No crashes or exceptions
   - [ ] Results match expected behavior (same as fresh run or clear migration)
   - [ ] No silent corruption (old data polluting new calculations)
   - [ ] Logging indicates old data was detected and handled

4. **Check output files:**
   - [ ] All new fields present in output
   - [ ] No degraded data quality (e.g., missing metrics)
   - [ ] Output matches fresh-run output (or documented differences)

**Example (from KAI-5):**

**Test:** Resume accuracy simulation from old intermediate folder
```bash
# Old folder created before ranking_metrics epic
ls simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/
# Contains: metadata.json with MAE only (no ranking_metrics)

# Run simulation (will try to resume from old folder)
python run_simulation.py

# Verify output
cat simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/metadata.json
# SHOULD contain ranking_metrics (not just MAE)
```

**Pass Criteria:**
- ✅ Old data doesn't prevent new metrics from being calculated
- ✅ Output files have ALL new fields (ranking_metrics present)
- ✅ No warnings about missing data
- ✅ Results match fresh run

**Why This Matters:** This test would have caught Issue #001 before user testing. Old files were loaded, polluted best_configs, and prevented ranking_metrics from being saved to output.
```

**Rationale:**
- Smoke tests only used fresh runs in KAI-5
- Resume scenario was completely untested until user testing
- This makes resume testing part of standard smoke test procedure

---

## Guide Update 5: Stage 6 Epic Smoke Testing - Add Resume Scenario

**File:** `feature-updates/guides_v2/stages/stage_6/epic_final_qc.md`

**Location:** Stage 6a: Epic Smoke Testing

**Current State:** Epic smoke testing focuses on feature integration but doesn't mention data compatibility

**Recommended Change:**

**Add to Stage 6a checklist (around line ~80, after "Run epic smoke test plan"):**

```markdown
### Data Compatibility Testing (if any feature touches persistence)

**Objective:** Verify epic works with data/files created before this epic started

**Checklist:**

- [ ] **Identify all persisted data modified by this epic:**
  - Configuration files
  - Intermediate results
  - Cached data
  - Database schemas

- [ ] **Test with pre-epic data:**
  - Use data created before epic started
  - Run epic functionality
  - Verify no crashes, corruption, or silent failures

- [ ] **Verify migration/handling:**
  - Old data is migrated (if migration implemented)
  - Old data is rejected with clear error (if incompatible)
  - Old data is ignored (if appropriate)
  - **NOT:** Old data is used but causes incorrect results

- [ ] **Document in epic_smoke_test_plan.md:**
  ```markdown
  ## Data Compatibility Test

  **Old Data Source:** [Where old data comes from]
  **Test Procedure:** [Steps to test with old data]
  **Expected Behavior:** [What should happen]
  **Pass Criteria:** [How to verify test passed]
  ```

**Example (KAI-5):**
```markdown
## Resume from Old Intermediate Folders

**Old Data:** accuracy_intermediate_* folders created Dec 23 (before ranking_metrics)
**Test Procedure:**
1. Run accuracy simulation (will detect old folders)
2. Check metadata.json in output
**Expected:** New folders have ranking_metrics (old folders ignored/overwritten)
**Pass Criteria:** All output files contain ranking_metrics
```
```

**Rationale:**
- Epic testing is final integration verification
- Should explicitly test compatibility with existing data
- Catches issues before user testing

---

## Implementation Priority

**High Priority (Implement Next):**
1. **Guide Update 1** - Add Iteration 7a to Stage 5a Round 1 (backward compatibility research)
   - Directly addresses root cause of Issue #001
   - Low effort, high impact
   - Estimated time: 15 min to update guide

2. **Guide Update 3** - Enhance Iteration 23a with design decision scrutiny
   - Would have caught MAE fallback flaw
   - Strengthens MANDATORY GATE
   - Estimated time: 10 min to update guide

**Medium Priority (Implement Soon):**
3. **Guide Update 2** - Add resume testing to Stage 5a Round 2
   - Makes backward compatibility testing explicit
   - Estimated time: 10 min to update guide

4. **Guide Update 4** - Add resume scenario to Stage 5c smoke testing
   - Catches resume bugs before epic testing
   - Estimated time: 10 min to update guide

**Lower Priority (Implement When Convenient):**
5. **Guide Update 5** - Add data compatibility to Stage 6 epic testing
   - Safety net for issues that slipped through Stage 5
   - Estimated time: 5 min to update guide

**Total Implementation Time:** ~50 minutes to update all 5 guides

---

## Success Metrics

**How to measure if updates are effective:**

1. **Backward compatibility issues caught earlier:**
   - Target: 0 backward compatibility bugs in Stage 6c (User Testing)
   - Measure: Track which stage catches compatibility issues

2. **Resume scenarios tested:**
   - Target: 100% of features with persistence have resume tests
   - Measure: Check todo.md for resume test scenarios

3. **Design decisions documented:**
   - Target: All fallback mechanisms have documented rationale + risks
   - Measure: Search spec.md for "Design Decision" sections

4. **Guide adherence:**
   - Target: 100% of epics complete new Iteration 7a
   - Measure: Check feature questions.md for backward compatibility analysis

---

## Related Issues

- **Issue #001** - This analysis is based on Issue #001 from KAI-5
- **Future Issues** - Track if similar bugs occur to validate effectiveness

---

## Notes for Guide Maintainers

**When implementing these updates:**

1. Update guide version numbers if using semantic versioning
2. Update prompts_reference_v2.md to include new iteration prompts
3. Update EPIC_WORKFLOW_USAGE.md with new examples
4. Consider adding backward compatibility checklist to reference cards
5. Update completion tracking in guides_v2/_internal/ (if applicable)

**Testing these updates:**

- Next epic should trial new Iteration 7a
- Collect feedback on whether it catches compatibility issues
- Refine based on real-world usage
- Update examples with actual findings from next epic

---

**Document Status:** Ready for Implementation
**Estimated Impact:** Prevents 1-2 user testing bugs per epic with backward compatibility requirements
**Cost/Benefit:** 50 min guide updates prevents hours of debugging per epic
