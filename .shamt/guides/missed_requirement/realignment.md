# PHASE 3 & 4: Realignment (S3) and Resume

**Purpose:** Re-align ALL features (S2.P2 + S3), then resume paused work (S4 deprecated — Test Scope Decision in S5 Step 0)

**When to Use:** After PHASE 2 complete, feature spec created/updated

**Previous Phase:** PHASE 2 (Planning) - See `missed_requirement/planning.md`

**Next Phase:** Resume previous work OR proceed to new/updated feature implementation (when its turn comes)

---

## Table of Contents

1. [Overview](#overview)
1. [PHASE 3: S2.P2 and S3 — Cross-Feature Alignment + Epic Approval](#phase-3-s2p2-and-s3--cross-feature-alignment--epic-approval)
   - [Part A: S2.P2 — Cross-Feature Alignment](#part-a-s2p2--cross-feature-alignment-pairwise-comparison)
   - [Step 1: Systematic Pairwise Comparison](#step-1-systematic-pairwise-comparison)
   - [Step 2: Identify Conflicts](#step-2-identify-conflicts)
   - [Step 3: Resolve Conflicts](#step-3-resolve-conflicts)
   - [Step 4: S2.P2 Complete — All Conflicts Resolved](#step-4-s2p2-complete--all-conflicts-resolved)
   - [Part B: S3 — Epic-Level Docs, Tests, and Approval](#part-b-s3--epic-level-docs-tests-and-approval)
   - [Step 5: S3.P1 — Update epic_smoke_test_plan.md](#step-5-s3p1--update-epic_smoke_test_planmd)
   - [Step 6: Update Existing Scenarios](#step-6-update-existing-scenarios)
   - [Step 7: Identify Integration Points](#step-7-identify-integration-points)
   - [Step 8: S3.P3 — Gate 4.5 Re-Approval](#step-8-s3p3--gate-45-re-approval)
1. [PHASE 4: Test Scope Decision (Replaces S4 — Deprecated)](#phase-4-test-scope-decision-replaces-s4--deprecated)
1. [PHASE 5: Resume Previous Work](#phase-5-resume-previous-work)
   - [Step 1: Mark Planning Complete](#step-1-mark-planning-complete)
1. [Missed Requirement Tracking](#missed-requirement-tracking)
1. [Current Status](#current-status)
   - [Step 2: Verify No Spec Changes Affect Paused Feature](#step-2-verify-no-spec-changes-affect-paused-feature)
   - [Step 3: Resume from Saved State](#step-3-resume-from-saved-state)
1. [Agent Status (PAUSED - Missed Requirement Handling)](#agent-status-paused---missed-requirement-handling)
1. [Agent Status (RESUMED)](#agent-status-resumed)
   - [Step 4: New/Updated Feature Implementation (Later)](#step-4-newupdated-feature-implementation-later)
1. [Completion Criteria](#completion-criteria)
1. [Common Scenarios](#common-scenarios)
   - [Scenario 1: New Feature - No Conflicts Found](#scenario-1-new-feature---no-conflicts-found)
   - [Scenario 2: New Feature - Minor Conflicts](#scenario-2-new-feature---minor-conflicts)
   - [Scenario 3: New Feature - Major Conflicts](#scenario-3-new-feature---major-conflicts)
   - [Scenario 4: Update Unstarted Feature](#scenario-4-update-unstarted-feature)
1. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
   - [❌ Anti-Pattern 1: Only Check New/Updated Feature](#-anti-pattern-1-only-check-newupdated-feature)
   - [❌ Anti-Pattern 2: Skip S3.P1](#-anti-pattern-2-skip-s3p1)
   - [❌ Anti-Pattern 3: Implementing Immediately](#-anti-pattern-3-implementing-immediately)
   - [❌ Anti-Pattern 4: Not Checking Paused Feature's Spec](#-anti-pattern-4-not-checking-paused-features-spec)
1. [Next Steps](#next-steps)

---

## Overview

**PHASE 3 & 4 ensures epic coherence after adding/updating a feature:**

- **S3:** Epic-Level Docs, Tests, and Approval (epic smoke test update + Gate 4.5 re-approval)
- **S4:** (Deprecated) Test Scope Decision now in S5 Step 0
- **Resume:** Return to paused work
- **Later:** Implement new/updated feature in sequence

---

## PHASE 3: S2.P2 and S3 — Cross-Feature Alignment + Epic Approval

### Part A: S2.P2 — Cross-Feature Alignment (Pairwise Comparison)

**🚨 FIRST ACTION:** Use "Starting S2.P2" prompt from `prompts/s2_prompts.md`

**READ:** `stages/s2/s2_p2_cross_feature_alignment.md`

**IMPORTANT:** Don't just check the new/updated feature — check ALL feature pairs

---

### Step 1: Systematic Pairwise Comparison

**Process:**

1. **New/updated feature vs ALL other features:**
   - New/updated feature vs feature_01
   - New/updated feature vs feature_02
   - New/updated feature vs feature_03
   - New/updated feature vs feature_04

2. **ALL other feature pairs** (may reveal issues):
   - feature_01 vs feature_02
   - feature_01 vs feature_03
   - feature_02 vs feature_03
   - Etc.

**For each pair, check:**
- Interface overlaps
- Data structure conflicts
- Duplicate functionality
- Integration dependencies
- Shared resources

---

### Step 2: Identify Conflicts

**Common conflict types:**

**Interface conflicts:**
```markdown
Issue: feature_02 and feature_05 both define PlayerData class
Resolution: Create shared PlayerData in utils, both features use it
```

**Data structure conflicts:**
```markdown
Issue: feature_03 expects player_id as string, feature_05 uses integer
Resolution: Standardize on integer across all features
```

**Duplicate functionality:**
```markdown
Issue: feature_04 has CSV export, now adding to feature_03
Resolution: Extract CSV export to shared utility, both features use it
```

**Integration dependencies:**
```markdown
Issue: feature_05 needs data from feature_02's projection API
Resolution: Document integration point, add to both specs
```

---

### Step 3: Resolve Conflicts

**For each conflict found:**

1. **Determine resolution approach:**
   - Update one feature's spec
   - Update both features' specs
   - Create shared utility
   - Refactor integration point

2. **Update affected feature specs:**
   - Document changes in spec.md
   - Update checklist.md with decision
   - Note why change was needed

3. **Get user approval for changes:**
   ```markdown
   During cross-feature re-alignment (S2.P2), I found a conflict:

   **Conflict:** {description}

   **Proposed Resolution:**
   {what needs to change}

   **Affected Features:**
   - feature_{XX}: {change needed}
   - feature_{YY}: {change needed}

   Approve this resolution? {User confirms}
   ```

---

### Step 4: S2.P2 Complete — All Conflicts Resolved

**After all conflicts resolved:**

```markdown
S2.P2 alignment complete (all cross-feature conflicts resolved).

**Features checked:** {count} features, {count} pairwise comparisons
**Conflicts found:** {count}
**Conflicts resolved:** {count}

**Changes made:**
- feature_{XX}: {changes}
- feature_{YY}: {changes}

**All features now aligned. Proceeding to S3 (Epic-Level Docs, Tests, and Approval).**
```

---

### Part B: S3 — Epic-Level Docs, Tests, and Approval

**🚨 FIRST ACTION:** Use "Starting S3" prompt from `prompts/s3_prompts.md`

**READ:** `stages/s3/s3_epic_planning_approval.md`

---

### Step 5: S3.P1 — Update epic_smoke_test_plan.md

**Questions to answer:**
- How does the new/updated feature integrate with other features?
- What epic-level workflows involve it?
- What should be tested in S9?
- What are the integration points?

**Add test scenarios for new/updated feature:**

```markdown
## Epic Integration Test: Item Scoring with Attribute Status

**Features involved:**
- feature_02 (projection_system)
- feature_05 (injury_tracking) ← NEW

**Scenario:**
1. Load item with attribute_status = "Questionable"
2. Generate projection (should reduce projected points)
3. Verify score reflects injury adjustment

**Expected:** Projection accounts for injury status
**Success criteria:** Degraded item score < healthy item score

**Data to verify:**
- Injury status field populated
- Projection reduction applied correctly
- Score calculation uses adjusted projection
```

---

### Step 6: Update Existing Scenarios

**Review existing test scenarios:**
- Do they need updates due to new/updated feature?
- New cross-feature workflows to test?
- Data flow changes?

**Update scenarios as needed:**

```markdown
## Epic Integration Test: Draft Recommendations (UPDATED)

**Features involved:**
- feature_01 (rank_integration)
- feature_02 (projection_system)
- feature_05 (injury_tracking) ← ADDED

**Scenario:**
1. Load items with rank data
2. Load injury status for each item ← NEW STEP
3. Generate projections (accounting for injuries) ← UPDATED
4. Generate scoring recommendations

**Expected:** Recommendations account for both rank priority and injury status
**Success criteria:** Degraded high-rank priority item ranked lower than healthy equivalent
```

---

### Step 7: Identify Integration Points

**Document integration points:**

```markdown
## Integration Points

**feature_02 → feature_05:**
- feature_02 calls feature_05.get_attribute_status(player_id)
- Returns: {"status": "Healthy|Questionable|Out", "impact_factor": 0.0-1.0}

**feature_05 → feature_02:**
- None (feature_05 doesn't call feature_02)

**Shared Data:**
- player_id (integer, standardized across all features)
- PlayerData class (utils/DataRecord.py)
```

---

### Step 8: S3.P3 — Gate 4.5 Re-Approval

**After S3.P1 (smoke test update) and S3.P2 (EPIC_README refinement) complete:**

```markdown
S3 re-alignment complete (cross-feature conflicts resolved + epic plan updated + Gate 4.5 re-approved).

**S2.P2 summary:** {count} features checked, {count} conflicts resolved
**S3.P1:** epic_smoke_test_plan.md updated with new/updated feature scenarios
**S3.P2:** EPIC_README.md updated
**Gate 4.5:** Epic plan re-approved

**All features are now aligned and epic plan is current.**

Proceed to S5 (Test Scope Decision + Implementation Planning for new/updated feature)? {User confirms}
```

---

## PHASE 4: Test Scope Decision (Replaces S4 — Deprecated)

> **⚠️ S4 is deprecated (SHAMT-6).** Do NOT run S4. Proceed directly to S5.

**At the start of S5 Step 0, do:**

1. Check Testing Approach (A/B/C/D) in EPIC_README
2. If Options C/D: identify algorithmic functions in the new/updated feature to unit test
3. If Options B/D: confirm Integration Test Convention in EPIC_README (set on a prior feature, or discover now)
4. Follow `stages/s5/s5_v2_validation_loop.md` Step 0 for the new/updated feature

**Note:** The epic_smoke_test_plan.md was already updated in PHASE 3 Part B (S3.P1). No separate test strategy document is needed.

---

## PHASE 5: Resume Previous Work

### Step 1: Mark Planning Complete

**Update EPIC_README.md:**

```markdown
## Missed Requirement Tracking

| # | Requirement | Action | Priority | Status | Created | Implemented | Notes |
|---|-------------|--------|----------|--------|---------|-------------|-------|
| 1 | Item attribute tracking | New feature_05 | High | PLANNING COMPLETE | 2026-01-04 | Not yet | Ready for implementation (after feature_02) |

## Current Status

**Last Updated:** {YYYY-MM-DD HH:MM}

**Planning Complete:**
- feature_05_injury_tracking spec created (S2 ✅)
- All features re-aligned (S3 ✅)
- Test Scope Decision done in S5 Step 0 (S4 deprecated) ✅

**Resuming Work:**
- feature_02_projection_system: Resuming S6
  - Resume from: {Exact step where paused}
  - Next action: {Continue implementation}
```

---

### Step 2: Verify No Spec Changes Affect Paused Feature

**Check:**
- Did S3 alignment change paused feature's spec?
- Does new/updated feature change interfaces paused feature uses?
- Do integration points affect paused feature?

---

#### If paused feature's spec WAS changed:

**Inform user:**

```markdown
I've completed planning for the missed requirement (Stages 2/3/4 complete).

During S3 alignment, feature_02's spec was updated:
- Added integration point: Call feature_05.get_attribute_status()
- Updated PlayerData class reference (now uses shared utility)
- Updated projection calculation to account for injury impact

Before resuming implementation, should I:
1. Update feature_02's implementation_plan.md to reflect spec changes
2. Continue with current implementation_plan.md (spec changes are minor/will handle during implementation)

What would you like to do?
```

**If user says update implementation_plan.md:**
- Re-run relevant parts of S5 for affected tasks
- Update implementation plan
- Document changes
- Then resume

---

#### If paused feature's spec was NOT changed:

**Inform user:**

```markdown
Planning complete for missed requirement.

Stages completed:
- S2: feature_05 spec created ✅
- S3: All features aligned ✅
- S4: Feature test strategy created ✅

feature_02's spec remains unchanged. Resuming implementation at S6.
```

---

### Step 3: Resume from Saved State

**Read paused feature's README.md:**

```markdown
## Agent Status (PAUSED - Missed Requirement Handling)

**Resume Instructions:**
When planning complete:
1. Verify this feature's spec still valid after alignment ← DID THIS
2. Resume at: S6 ← RESUME HERE
3. Context: Implementing projection calculation logic ← CONTEXT
```

**Update paused feature's README Agent Status:**

```markdown
## Agent Status (RESUMED)

**Last Updated:** {YYYY-MM-DD HH:MM}

**Current Phase:** IMPLEMENTATION_EXECUTION (Resumed)
**Current Guide:** stages/s6/s6_execution.md

**Resumed After:** Missed requirement planning complete
- feature_05_injury_tracking spec created and aligned
- Stages 2/3/4 complete for feature_05
- feature_02 spec verified (unchanged/updated)

**Current Stage:** S6 (Implementation Execution)
**Next Action:** Continue S6 execution - Projection calculation logic

**Critical Rules from Guide:**
- Keep spec.md visible during implementation
- Continuous verification against spec
- Mini-QC checkpoints
- 100% test pass required
```

**Continue where you left off**

---

### Step 4: New/Updated Feature Implementation (Later)

**Important:** Don't implement new/updated feature yet!

**Implementation happens later when its turn comes in sequence:**

**Example - Medium Priority:**
```text
Sequence:
1. feature_01 ✅ COMPLETE
2. feature_02 🔄 RESUMED (continue now)
3. feature_05 ◻️ NOT STARTED (implement after feature_02 completes)
4. feature_03 ◻️ NOT STARTED
5. feature_04 ◻️ NOT STARTED

Current action: Complete feature_02 (S6 → S7 → S8)
After feature_02: Implement feature_05 (S5 → S6 → S7 → S8)
```

**Example - High Priority:**
```bash
Sequence (high priority inserted):
1. feature_01 ✅ COMPLETE
2. feature_05 ◻️ NOT STARTED (implement immediately - blocks feature_02)
3. feature_02 🔄 PAUSED (resume after feature_05 completes)
4. feature_03 ◻️ NOT STARTED
5. feature_04 ◻️ NOT STARTED

Current action: Implement feature_05 (S5 → S6 → S7 → S8)
After feature_05: Resume and complete feature_02
```

**When new/updated feature's turn comes:**
- Run full S5 (S5 → S6 → S7 → S8)
- Same rigor as all features
- No shortcuts

---

## Completion Criteria

**PHASE 3 & 4 complete when:**

**S2.P2 (Cross-Feature Alignment):**
- [x] All feature pairs compared systematically
- [x] All conflicts identified
- [x] All conflicts resolved
- [x] Affected specs updated
- [x] User approved conflict resolutions
- [x] S2.P2 sign-off complete

**S3 (Epic-Level Docs, Tests, and Approval):**
- [x] epic_smoke_test_plan.md updated (S3.P1)
- [x] New scenarios added for new/updated feature
- [x] Existing scenarios updated if needed
- [x] Integration points documented
- [x] EPIC_README.md refined (S3.P2)
- [x] Gate 4.5 re-approval obtained (S3.P3)

**S4 (deprecated — test scope decision now at S5 Step 0 for Options C/D):**
- [x] Test scope confirmed per Testing Approach (A/B/C/D from EPIC_README)

**Resume:**
- [x] EPIC_README.md updated (planning complete)
- [x] Paused feature spec verified (changed or unchanged)
- [x] If changed: User decision on implementation_plan.md update
- [x] Paused feature README updated (resumed status)
- [x] Work resumed at correct point

---

## Common Scenarios

### Scenario 1: New Feature - No Conflicts Found

**Actions:**
1. Run cross-feature re-alignment (S2.P2 pairwise comparison, then S3 approval)
2. No conflicts found
3. User signs off
4. Update epic smoke test plan in S3.P1, then proceed to S5 (test scope decision at S5 Step 0 — S4 deprecated)
5. Resume paused work
6. New feature implemented later in sequence

---

### Scenario 2: New Feature - Minor Conflicts

**Actions:**
1. Run cross-feature re-alignment (S2.P2 pairwise comparison, then S3 approval)
2. Find minor conflicts (e.g., naming inconsistency)
3. Resolve conflicts (update specs)
4. User approves resolutions
5. Update epic smoke test plan in S3.P1, then proceed to S5 (test scope decision at S5 Step 0 — S4 deprecated)
6. Resume paused work (spec unchanged)
7. New feature implemented later

---

### Scenario 3: New Feature - Major Conflicts

**Actions:**
1. Run cross-feature re-alignment (S2.P2 pairwise comparison, then S3 approval)
2. Find major conflicts (e.g., duplicate functionality)
3. Resolve conflicts (extract to shared utility)
4. Update multiple feature specs
5. User approves resolutions
6. Update epic smoke test plan in S3.P1, then proceed to S5 (test scope decision at S5 Step 0 — S4 deprecated)
7. Resume paused work (spec WAS changed)
8. User decides: Update implementation_plan.md or handle during implementation
9. New feature implemented later

---

### Scenario 4: Update Unstarted Feature

**Actions:**
1. Run cross-feature re-alignment (S2.P2 pairwise comparison, then S3 approval)
2. Check updated feature vs all others
3. Resolve any conflicts
4. Update epic smoke test plan in S3.P1, then proceed to S5 (test scope decision at S5 Step 0 — S4 deprecated)
5. Resume paused work (if any)
6. Updated feature implemented later (in its original sequence position)

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Only Check New/Updated Feature

**Mistake:** "I'll just check the new feature vs others, skip other pairs"

**Why wrong:** New feature may reveal conflicts between existing features

**Correct:** Check ALL feature pairs systematically

---

### ❌ Anti-Pattern 2: Skip S3.P1 Test Plan Update

**Mistake:** "It's a small feature — skip the epic smoke test update"

**Why wrong:** Even small features need epic-level test coverage (S3.P1); for Options C/D, test scope is decided at S5 Step 0

**Correct:** Always update epic_smoke_test_plan.md in S3.P1; for Options C/D, define test scope at S5 Step 0 (S4 deprecated)

---

### ❌ Anti-Pattern 3: Implementing Immediately

**Mistake:** After planning, immediately implement new feature before resuming paused work

**Why wrong:** Breaks sequence, paused work left incomplete

**Correct:** Resume paused work, implement new/updated feature when its turn comes

---

### ❌ Anti-Pattern 4: Not Checking Paused Feature's Spec

**Mistake:** Resume without checking if paused feature's spec changed

**Why wrong:** May be implementing against outdated spec

**Correct:** Always verify paused feature's spec after S3

---

## Next Steps

**After completing PHASE 3 & 4 (Realignment and Resume):**

✅ S2.P2 complete (cross-feature conflicts resolved)
✅ S3 complete (epic test plan updated + Gate 4.5 re-approved)
✅ S4 (deprecated — test scope decision now at S5 Step 0)
✅ Paused feature spec verified
✅ Work resumed OR ready to resume

**Next:**
- If work was paused: Continue paused feature implementation
- If work was not paused: Continue current feature implementation
- Later: When new/updated feature's turn comes, implement through full S5

**Special Case:**
- If discovered during S9/S10: See `missed_requirement/s9_s10_special.md`

---

**END OF PHASE 3 & 4 GUIDE**
