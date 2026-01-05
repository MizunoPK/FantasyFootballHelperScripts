# STAGE 4: Epic Testing Strategy - Quick Reference Card

**Purpose:** One-page summary for updating epic test plan with concrete scenarios
**Use Case:** Quick lookup when transforming placeholder test plan into actionable tests
**Total Time:** 30-45 minutes

---

## Workflow Overview

```
STEP 1: Review Initial Test Plan (5 min)
    ├─ Read epic_smoke_test_plan.md (Stage 1 version)
    ├─ Identify placeholders and assumptions
    └─ Note what needs updating
    ↓
STEP 2: Identify Integration Points (10-15 min)
    ├─ Review all feature specs
    ├─ Map data flows between features
    ├─ Identify shared resources (files, config, classes)
    └─ Document integration points
    ↓
STEP 3: Define Epic Success Criteria (5-10 min)
    ├─ Based on original epic request
    ├─ Based on approved feature plan (Stage 3)
    ├─ Make criteria MEASURABLE (not vague)
    └─ Document what "success" looks like
    ↓
STEP 4: Create Specific Test Scenarios (10-15 min)
    ├─ Convert high-level categories to concrete tests
    ├─ Add specific commands to run
    ├─ Define expected outputs
    └─ Document failure indicators
    ↓
STEP 5: Update epic_smoke_test_plan.md (5-10 min)
    ├─ Replace placeholder content
    ├─ Add all new sections
    ├─ Mark as "Stage 4 version - will update in Stage 5e"
    └─ Update Update Log (what changed from Stage 1)
    ↓
STEP 6: Mark Complete (2 min)
    ├─ Update epic EPIC_README.md (Stage 4 complete)
    └─ Transition to Stage 5
```

---

## Step Summary Table

| Step | Duration | Key Activities | Outputs | Gate? |
|------|----------|----------------|---------|-------|
| 1 | 5 min | Review Stage 1 test plan | List of updates needed | No |
| 2 | 10-15 min | Identify integration points | Integration point map | No |
| 3 | 5-10 min | Define measurable success criteria | Epic success criteria | No |
| 4 | 10-15 min | Create concrete test scenarios | Test scenarios | No |
| 5 | 5-10 min | Update epic_smoke_test_plan.md | Updated test plan | No |
| 6 | 2 min | Mark complete | EPIC_README updated | No |

---

## Test Plan Evolution

### Stage 1 Version (Placeholder)
**Based on:** Assumptions (no specs yet)
**Content:**
- High-level categories (vague)
- "TBD" for specific commands
- Not measurable criteria

**Example:**
```markdown
## Success Criteria (INITIAL - WILL REFINE)
- Draft helper uses new data sources (vague)
- Recommendations are more accurate (not measurable)

## Test 1: Run Draft Helper
# Command TBD after Stage 2 deep dives
**Expected:** TBD
```

### Stage 4 Version (Concrete)
**Based on:** Actual feature specs (after Stage 2/3)
**Content:**
- Specific test scenarios
- Real commands from specs
- Measurable success criteria

**Example:**
```markdown
## Epic Success Criteria
- All 4 features create expected output files
- FantasyPlayer has all new fields (adp_value, injury_status, schedule_strength)
- Final recommendations include all multipliers

## Test 1: End-to-End Integration
```bash
python run_league_helper.py --mode draft
```
**Expected:** recommendations.csv with 3 new columns (adp_multiplier, injury_multiplier, schedule_strength)
```

### Stage 5e Version (Refined)
**Based on:** Actual implementation (after each feature completes)
**Content:**
- Updated after EACH feature implementation
- Reflects reality (not plans)
- Integration scenarios discovered during coding

**Note:** Stage 4 → Stage 5e evolution happens incrementally (update after each feature)

---

## Integration Point Categories

### Type 1: Shared Data Structures
**What:** Multiple features modify same class/file
**Example:** Features 1, 2, 3 all add fields to FantasyPlayer
**Test Need:** Verify all fields present after all features run

### Type 2: Computational Dependencies
**What:** Feature B depends on Feature A's calculations
**Example:** Feature 4 (recommendations) needs Feature 1's ADP multiplier
**Test Need:** Verify calculation order and result propagation

### Type 3: File Dependencies
**What:** Feature B reads file created by Feature A
**Example:** Feature 4 reads data/rankings/adp.csv created by Feature 1
**Test Need:** Verify file exists, format correct, data valid

### Type 4: Configuration Dependencies
**What:** Features share config keys
**Example:** Features 2 and 3 both use THRESHOLD config key
**Test Need:** Verify no config conflicts, correct values loaded

### Type 5: Shared Resources
**What:** Features access same external resources
**Example:** Both features use same API endpoint
**Test Need:** Verify resource not corrupted, concurrent access works

---

## Measurable vs Vague Criteria

### ❌ Vague (Stage 1)
- "Feature works"
- "Recommendations are better"
- "No errors occur"
- "Players are ranked correctly"

### ✅ Measurable (Stage 4)
- "All 4 features create expected output files (list files)"
- "Recommendations.csv has 3 new columns (name them)"
- "0 errors in console output during E2E test"
- "Top 10 players include ADP rank ≤ 15"

---

## Critical Rules Summary

- ✅ Stage 3 (user approval) MUST be complete before Stage 4
- ✅ epic_smoke_test_plan.md is MAJOR UPDATE (not minor tweak)
- ✅ Identify ALL integration points between features
- ✅ Define MEASURABLE success criteria (not vague)
- ✅ Test plan will update AGAIN in Stage 5e (mark clearly)
- ✅ Include both feature-level AND epic-level tests
- ✅ Mark update in Update Log (what changed, why)
- ✅ Update epic EPIC_README.md Epic Completion Checklist

---

## Common Pitfalls

### ❌ Pitfall 1: Copying Stage 1 Placeholders
**Problem:** "Stage 1 test plan looks good, I'll keep it"
**Impact:** Tests are vague, can't verify epic success in Stage 6
**Solution:** REPLACE placeholders with concrete scenarios from specs

### ❌ Pitfall 2: Vague Success Criteria
**Problem:** "Epic succeeds if all features work"
**Impact:** Can't objectively verify success, subjective testing
**Solution:** Define MEASURABLE criteria (file counts, field names, specific outputs)

### ❌ Pitfall 3: Missing Integration Points
**Problem:** "I'll just test each feature individually"
**Impact:** Integration bugs slip through, fail in Stage 6
**Solution:** Identify ALL integration points, create integration tests

### ❌ Pitfall 4: Not Marking as "Stage 4 Version"
**Problem:** Treating Stage 4 test plan as final
**Impact:** Forget to update in Stage 5e, test plan out of sync with code
**Solution:** Mark clearly "Stage 4 version - will update in Stage 5e"

### ❌ Pitfall 5: Forgetting Feature-Level Tests
**Problem:** Only defining epic-level tests
**Impact:** Can't isolate which feature is failing
**Solution:** Include BOTH feature-level (individual) AND epic-level (integration) tests

### ❌ Pitfall 6: Not Documenting Changes
**Problem:** Updating test plan without explaining what changed
**Impact:** No history, can't understand evolution
**Solution:** Update Update Log with Stage 1 → Stage 4 changes

---

## Quick Checklist: "Am I Ready for Next Step?"

**Before Step 1:**
- [ ] Stage 3 complete (user approved plan)
- [ ] All feature specs finalized
- [ ] epic_smoke_test_plan.md exists (from Stage 1)
- [ ] Have read all feature specs

**Step 1 → Step 2:**
- [ ] Reviewed Stage 1 test plan
- [ ] Identified placeholders
- [ ] Listed sections needing updates

**Step 2 → Step 3:**
- [ ] All feature specs reviewed
- [ ] Data flows mapped
- [ ] Integration points documented
- [ ] Shared resources identified

**Step 3 → Step 4:**
- [ ] Success criteria based on epic request
- [ ] Success criteria based on approved plan
- [ ] All criteria are MEASURABLE
- [ ] Documented what "success" looks like

**Step 4 → Step 5:**
- [ ] High-level categories converted to concrete tests
- [ ] Specific commands added (from specs)
- [ ] Expected outputs defined
- [ ] Failure indicators documented

**Step 5 → Step 6:**
- [ ] epic_smoke_test_plan.md updated
- [ ] Marked as "Stage 4 version - will update in Stage 5e"
- [ ] Update Log updated (what changed from Stage 1, why)
- [ ] Both feature-level and epic-level tests included

**Step 6 → Stage 5:**
- [ ] epic EPIC_README.md updated (Stage 4 complete)
- [ ] Agent Status updated (next: Stage 5)

---

## File Outputs

**Step 2:**
- Integration point map (in epic_smoke_test_plan.md or research/)

**Step 3:**
- Epic success criteria (measurable)

**Step 4:**
- Concrete test scenarios

**Step 5:**
- Updated epic_smoke_test_plan.md with:
  - Epic Success Criteria (measurable)
  - Specific Commands/Scenarios (concrete)
  - Integration Points
  - Feature-Level Tests
  - Epic-Level Tests
  - Update Log entry

---

## Test Plan Structure

**Recommended sections in epic_smoke_test_plan.md:**

1. **Version Marker**
   - "Stage 4 version - will update in Stage 5e"

2. **Epic Success Criteria**
   - Measurable criteria (3-5 items)

3. **Integration Points**
   - List of all integration points
   - Features involved per point
   - What needs testing

4. **Feature-Level Tests**
   - Test each feature individually
   - Commands to run
   - Expected outputs

5. **Epic-Level Tests**
   - Test features working together
   - End-to-end workflows
   - Cross-feature data flows

6. **Update Log**
   - Stage 1 → Stage 4 changes
   - Rationale for changes
   - What sections updated

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting Stage 4 | stages/stage_4/epic_testing_strategy.md |
| Need integration point examples | stages/stage_4/epic_testing_strategy.md (Step 2) |
| Need test scenario templates | stages/stage_4/epic_testing_strategy.md (Step 4) |

---

## Exit Conditions

**Stage 4 is complete when:**
- [ ] epic_smoke_test_plan.md contains specific test scenarios (not placeholders)
- [ ] All integration points documented
- [ ] Success criteria are measurable
- [ ] Both feature-level and epic-level tests defined
- [ ] Specific commands included
- [ ] Expected outputs defined
- [ ] Marked as "Stage 4 version - will update in Stage 5e"
- [ ] Update Log documents changes from Stage 1
- [ ] epic EPIC_README.md shows Stage 4 complete
- [ ] Ready to start Stage 5 (Feature Implementation)

**Next Stage:** Stage 5 (Feature Implementation) - start with first feature

---

**Last Updated:** 2026-01-04
