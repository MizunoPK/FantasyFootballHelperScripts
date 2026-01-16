# STAGE 4: Epic Testing Strategy - Quick Reference Card

**Purpose:** One-page summary for updating epic test plan with concrete scenarios
**Use Case:** Quick lookup when transforming placeholder test plan into actionable tests
**Total Time:** 30-45 minutes (agent work) + user approval time

---

## Workflow Overview

```
STEP 1: Review Initial Test Plan (5 min)
    ├─ Read epic_smoke_test_plan.md (S1 version)
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
    ├─ Based on approved feature plan (S3)
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
    ├─ Mark as "S4 version - will update in S8.P2"
    └─ Update Update Log (what changed from S1)
    ↓
STEP 6: Mark Complete (2 min + user approval time)
    ├─ Update epic EPIC_README.md (S4 complete)
    ├─ 🚨 Gate 4.5: Present test plan to user (MANDATORY)
    ├─ Wait for user approval
    └─ Transition to S5
```

---

## Step Summary Table

| Step | Duration | Key Activities | Outputs | Gate? |
|------|----------|----------------|---------|-------|
| 1 | 5 min | Review S1 test plan | List of updates needed | No |
| 2 | 10-15 min | Identify integration points | Integration point map | No |
| 3 | 5-10 min | Define measurable success criteria | Epic success criteria | No |
| 4 | 10-15 min | Create concrete test scenarios | Test scenarios | No |
| 5 | 5-10 min | Update epic_smoke_test_plan.md | Updated test plan | No |
| 6 | 2 min + user time | Mark complete + user approval | EPIC_README updated | **YES - Gate 4.5** |

---

## Test Plan Evolution

### S1 Version (Placeholder)
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
# Command TBD after S2 deep dives
**Expected:** TBD
```

### S4 Version (Concrete)
**Based on:** Actual feature specs (after S2/3)
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

### S8.P2 Version (Refined)
**Based on:** Actual implementation (after each feature completes)
**Content:**
- Updated after EACH feature implementation
- Reflects reality (not plans)
- Integration scenarios discovered during coding

**Note:** S4 → S8.P2 evolution happens incrementally (update after each feature)

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

### ❌ Vague (S1)
- "Feature works"
- "Recommendations are better"
- "No errors occur"
- "Players are ranked correctly"

### ✅ Measurable (S4)
- "All 4 features create expected output files (list files)"
- "Recommendations.csv has 3 new columns (name them)"
- "0 errors in console output during E2E test"
- "Top 10 players include ADP rank ≤ 15"

---

## Critical Rules Summary

- ✅ S3 (user approval) MUST be complete before S4
- ✅ epic_smoke_test_plan.md is MAJOR UPDATE (not minor tweak)
- ✅ Identify ALL integration points between features
- ✅ Define MEASURABLE success criteria (not vague)
- ✅ Test plan will update AGAIN in S8.P2 (mark clearly)
- ✅ Include both feature-level AND epic-level tests
- ✅ Mark update in Update Log (what changed, why)
- ✅ Update epic EPIC_README.md Epic Completion Checklist
- ✅ 🚨 **Gate 4.5: User MUST approve test plan before S5 (MANDATORY)**

---

## Common Pitfalls

### ❌ Pitfall 1: Copying S1 Placeholders
**Problem:** "S1 test plan looks good, I'll keep it"
**Impact:** Tests are vague, can't verify epic success in S9
**Solution:** REPLACE placeholders with concrete scenarios from specs

### ❌ Pitfall 2: Vague Success Criteria
**Problem:** "Epic succeeds if all features work"
**Impact:** Can't objectively verify success, subjective testing
**Solution:** Define MEASURABLE criteria (file counts, field names, specific outputs)

### ❌ Pitfall 3: Missing Integration Points
**Problem:** "I'll just test each feature individually"
**Impact:** Integration bugs slip through, fail in S9
**Solution:** Identify ALL integration points, create integration tests

### ❌ Pitfall 4: Not Marking as "S4 Version"
**Problem:** Treating S4 test plan as final
**Impact:** Forget to update in S8.P2, test plan out of sync with code
**Solution:** Mark clearly "S4 version - will update in S8.P2"

### ❌ Pitfall 5: Forgetting Feature-Level Tests
**Problem:** Only defining epic-level tests
**Impact:** Can't isolate which feature is failing
**Solution:** Include BOTH feature-level (individual) AND epic-level (integration) tests

### ❌ Pitfall 6: Not Documenting Changes
**Problem:** Updating test plan without explaining what changed
**Impact:** No history, can't understand evolution
**Solution:** Update Update Log with S1 → S4 changes

---

## Quick Checklist: "Am I Ready for Next Step?"

**Before Step 1:**
- [ ] S3 complete (user approved plan)
- [ ] All feature specs finalized
- [ ] epic_smoke_test_plan.md exists (from S1)
- [ ] Have read all feature specs

**Step 1 → Step 2:**
- [ ] Reviewed S1 test plan
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
- [ ] Marked as "S4 version - will update in S8.P2"
- [ ] Update Log updated (what changed from S1, why)
- [ ] Both feature-level and epic-level tests included

**Step 6 → S5:**
- [ ] epic EPIC_README.md updated (S4 complete)
- [ ] 🚨 Gate 4.5: epic_smoke_test_plan.md presented to user (MANDATORY)
- [ ] User approved test plan
- [ ] Gate 4.5 marked ✅ PASSED in EPIC_README.md
- [ ] Agent Status updated (next: S5)

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
   - "S4 version - will update in S8.P2"

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
   - S1 → S4 changes
   - Rationale for changes
   - What sections updated

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting S4 | stages/s4/s4_epic_testing_strategy.md |
| Need integration point examples | stages/s4/s4_epic_testing_strategy.md (Step 2) |
| Need test scenario templates | stages/s4/s4_epic_testing_strategy.md (Step 4) |

---

## Exit Conditions

**S4 is complete when:**
- [ ] epic_smoke_test_plan.md contains specific test scenarios (not placeholders)
- [ ] All integration points documented
- [ ] Success criteria are measurable
- [ ] Both feature-level and epic-level tests defined
- [ ] Specific commands included
- [ ] Expected outputs defined
- [ ] Marked as "S4 version - will update in S8.P2"
- [ ] Update Log documents changes from S1
- [ ] epic EPIC_README.md shows S4 complete
- [ ] 🚨 **Gate 4.5: User approved epic_smoke_test_plan.md (MANDATORY)**
- [ ] Gate 4.5 marked ✅ PASSED in EPIC_README.md
- [ ] Ready to start S5 (Feature Implementation)

**Next Stage:** S5 (Feature Implementation) - start with first feature

---

**Last Updated:** 2026-01-10
