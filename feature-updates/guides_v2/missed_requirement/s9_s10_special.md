# SPECIAL CASE: Discovery During Epic Testing (S9/7)

**Purpose:** Handle missed requirements discovered during epic testing with special restart protocol

**When to Use:** Missed requirement discovered during S9 (Epic Testing) or S10 (User Testing)

**Previous Phase:** PHASE 3 & 4 (Realignment) - See `missed_requirement/realignment.md`

**Next Phase:** Restart epic testing from S9.P1 Step 1

---

## Why This is Different

**Normal workflow (discovered during S5):**
- Plan new/updated feature (Stages 2/3/4)
- Resume paused work
- Implement features in sequence
- Continue to next stage when turn comes

**Special case (discovered during S9/7):**
- Plan new/updated feature (Stages 2/3/4) ← SAME
- Resume any paused work
- **Complete ALL remaining features first** ← DIFFERENT
- **Implement new/updated feature (full S5)** ← DIFFERENT
- **RESTART epic testing from S9.P1 Step 1** ← DIFFERENT

---

## Why Restart Epic Testing?

**Rationale:**

1. **Epic integration changes:**
   - New feature changes how features work together
   - Previous epic test results may be invalid
   - Need to re-verify entire epic with new feature

2. **Test coverage completeness:**
   - Epic smoke tests need to include new feature
   - Epic QC rounds need to cover new integration points
   - Can't assume previous tests still valid

3. **Quality assurance:**
   - Same rigor as initial epic testing
   - Ensures epic coherence
   - Prevents integration issues in production

**Similar to debugging protocol's loop-back mechanism:**
- Debugging: Fix issues → Loop back to smoke testing
- Missed requirement: Add feature → Loop back to epic testing

---

## Workflow Overview

```text
Discovery (S9.P2: Epic QC Round 1)
    ↓
PHASE 1: Discovery & User Decision (normal)
    ↓
PHASE 2: Planning - S2 Deep Dive (normal)
    ↓
PHASE 3 & 4: Realignment - S3 & 4 (normal)
    ↓
SPECIAL: Complete ALL Remaining Features
    ↓
SPECIAL: Implement New/Updated Feature (full S5)
    ↓
SPECIAL: RESTART Epic Testing from S9.P1 Step 1
    ↓
S9.P1 → S9.P2 → S9.P3 → S10 (entire epic flow)
```markdown

---

## Step-by-Step Process

### Step 1-3: Normal Process (PHASE 1-4)

**Follow normal missed requirement workflow:**

1. **PHASE 1:** Discovery & User Decision
   - Use `missed_requirement/discovery.md`
   - Present options to user
   - Get decision on approach
   - Document paused work (epic testing paused)

2. **PHASE 2:** Planning (S2)
   - Use `missed_requirement/planning.md`
   - Create/update feature spec
   - Full S2 rigor

3. **PHASE 3 & 4:** Realignment (S3 & 4)
   - Use `missed_requirement/realignment.md`
   - Cross-feature sanity check
   - Update epic test plan
   - **Note:** Epic testing is paused, not a specific feature

---

### Step 4: Complete ALL Remaining Features

**After planning complete (Stages 2/3/4), DON'T return to epic testing:**

**Identify remaining features:**

```markdown
Current state:
- feature_01 ✅ COMPLETE
- feature_02 ✅ COMPLETE
- feature_03 🔄 PAUSED (was implementing when entered S9)
- feature_04 ◻️ NOT STARTED
- feature_05 ◻️ NOT STARTED (NEW - from missed requirement)

Actions needed:
1. Resume and complete feature_03 (S5 → complete)
2. Implement feature_04 (full S5)
3. Implement feature_05 (full S5)
4. Then restart epic testing
```markdown

**Complete each feature in sequence:**
- Resume feature_03 where it left off
- Run through S5 (S5 → S6 → S7 → S8) for feature_03
- Implement feature_04 (full S5)
- Implement feature_05 (full S5)
- **ALL features must be complete before restarting epic testing**

---

### Step 5: Implement New/Updated Feature

**When new/updated feature's turn comes in sequence:**

**Run full S5:**
- S5: TODO Creation (3 rounds, 22 iterations)
- S6: Implementation Execution
- S7: Post-Implementation (smoke testing, QC rounds, final review)
- S8.P1: Cross-Feature Spec Alignment
- S8.P2: Epic Testing Plan Reassessment

**Same rigor as all features:**
- No shortcuts
- All rounds and iterations
- 100% test pass required
- Complete documentation

---

### Step 6: RESTART Epic Testing from S9.P1 Step 1

**Critical: Don't resume epic testing mid-stream**

**Why restart from beginning:**
- New feature changes epic integration
- Previous test results (Stages S9.P1/S9.P2) are invalid
- Need clean epic test pass with new feature included

**Update EPIC_README.md:**

```markdown
## Current Status

**Last Updated:** {YYYY-MM-DD HH:MM}

**All Features Complete:**
- feature_01 ✅
- feature_02 ✅
- feature_03 ✅
- feature_04 ✅
- feature_05 ✅ (from missed requirement)

**Restarting Epic Testing:**
- Reason: feature_05 added during previous epic testing
- Previous epic test progress: S9.P2 Round 1 (discarded)
- Restarting from: S9.P1 Step 1 (Epic Smoke Testing)

**Next Action:** Execute epic smoke test plan with ALL 5 features
```markdown

**Follow S9 from beginning:**

**🚨 FIRST ACTION:** Use "Starting S9" prompt from `prompts/s9_prompts.md`

**READ:** `stages/s9/s9_epic_final_qc.md`

**Execute:**
1. **S9.P1:** Epic Smoke Testing (Part 1-4)
   - Part 1: Import Test (all features)
   - Part 2: Entry Point Test
   - Part 3: E2E Execution Test
   - Part 4: Cross-Feature Integration Test ← **Includes new feature**

2. **S9.P2:** Epic QC Rounds (Round 1-3)
   - Round 1: Cross-Feature Integration
   - Round 2: Epic Cohesion & Consistency
   - Round 3: End-to-End Success Criteria

3. **S9.P3:** Epic Final Review
   - Code review
   - Documentation review
   - Epic readiness check

4. **S10:** Epic Cleanup
   - User testing ← **User tests with new feature**
   - Commit and merge
   - Archive

---

## Examples

### Example 1: Discovery During S9.P2 (Epic QC Round 1)

```markdown
**Context:**
- Epic: Fantasy Football Helpers
- Stage: S9.P2 (Epic QC Round 1)
- Features complete: feature_01, feature_02, feature_03
- Features not started: feature_04
- Discovery: Missing caching layer needed for feature_02/feature_03 integration

**Workflow:**

1. **Discovery:** Present options to user
   - Option 1: Create new feature_05_caching_layer
   - Option 2: Update feature_04
   - User chooses: Create new feature (medium priority)

2. **Planning:** S2/3/4
   - Create feature_05 spec
   - Align all features
   - Update epic test plan

3. **Complete remaining features:**
   - Implement feature_04 (S5 → S8)
   - Implement feature_05 (S5 → S8)

4. **Restart epic testing:**
   - S9.P1 Part 1 (Import Test) - all 5 features
   - S9.P1 Part 2 (Entry Point Test)
   - S9.P1 Part 3 (E2E Test)
   - S9.P1 Part 4 (Cross-Feature Integration) - includes caching layer
   - S9.P2 (QC Rounds)
   - S9.P3 (Final Review)
   - S10 (Cleanup & User Testing)
```markdown

---

### Example 2: Discovery During S10 (User Testing)

```markdown
**Context:**
- Epic: Fantasy Football Helpers
- Stage: 7 (User Testing)
- All features: COMPLETE
- User reports: "Missing export to PDF functionality"

**Workflow:**

1. **Discovery:** Present options to user
   - Option 1: Create new feature_05_pdf_export
   - Option 2: Update feature_03_performance_tracker
   - User chooses: Update feature_03 (logical grouping)

2. **Planning:** S2/3/4
   - Update feature_03 spec with PDF export
   - Align all features
   - Update epic test plan

3. **Complete remaining features:**
   - No remaining features
   - Re-implement feature_03 with new scope (S5 → S8)

4. **Restart epic testing:**
   - S9.P1 (Epic Smoke Testing) - feature_03 now includes PDF export
   - S9.P2 (Epic QC Rounds)
   - S9.P3 (Epic Final Review)
   - S10 (User Testing) - user tests again with PDF export

**Note:** Even though discovered in S10, loop back to S9.P1 (not S10)
```

---

## Comparison: Normal vs Special Case

| Aspect | Normal (S5) | Special (S9/7) |
|--------|-----------------|---------------------|
| **Planning** | Stages 2/3/4 ✓ | Stages 2/3/4 ✓ |
| **Resume paused work** | Resume feature implementation | Not applicable (features done) |
| **Complete remaining features** | Not required | **REQUIRED - ALL features** |
| **Implement new/updated feature** | When its turn comes in sequence | **After all remaining features** |
| **Return to** | Resume where left off | **Restart S9.P1 Step 1** |
| **Epic testing** | Not affected (happens later) | **Completely restarted** |

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Resuming Epic Testing Mid-Stream

**Mistake:** After implementing new feature, resume S9.P2 Round 1 (where left off)

**Why wrong:** Previous epic test results invalid with new feature

**Correct:** Restart from S9.P1 Step 1

---

### ❌ Anti-Pattern 2: Skipping Remaining Features

**Mistake:** "feature_04 is small, I'll skip it and just implement the new feature"

**Why wrong:** Epic incomplete, can't proceed to epic testing

**Correct:** Complete ALL remaining features before implementing new/updated feature

---

### ❌ Anti-Pattern 3: Partial Epic Re-Testing

**Mistake:** "I'll just re-run the integration tests affected by new feature"

**Why wrong:** Missing epic-level validation, potential issues elsewhere

**Correct:** Run complete S9 (S9.P1 → S9.P2 → S9.P3 → S9.P4) from beginning

---

### ❌ Anti-Pattern 4: Returning to S10 After Fixes

**Mistake:** User finds bug in S10 → Fix → Resume S10

**Why wrong:** Fixes might affect epic integration, need epic-level validation

**Correct:** User finds bug → Fix → Restart S9.P1 → S10

---

## Completion Criteria

**Special case workflow complete when:**

**Planning:**
- [x] PHASE 1-4 complete (normal workflow)
- [x] New/updated feature spec created
- [x] All features aligned
- [x] Epic test plan updated

**Feature Completion:**
- [x] ALL remaining features completed (full S5 each)
- [x] New/updated feature implemented (full S5)
- [x] All features passing tests (100%)
- [x] Epic Progress Tracker shows all features complete

**Epic Testing Restart:**
- [x] S9.P1 complete (Epic Smoke Testing with new feature)
- [x] S9.P2 complete (Epic QC Rounds)
- [x] S9.P3 complete (Epic Final Review)
- [x] Ready for S10 (User Testing with new feature)

---

## Summary

**Special case for S9/7 discovery:**

1. Follow normal PHASE 1-4 (discovery, planning, realignment)
2. **Different:** Complete ALL remaining features first
3. **Different:** Implement new/updated feature (full S5)
4. **Different:** RESTART epic testing from S9.P1 Step 1
5. Run complete epic testing flow (S9.P1 → S9.P2 → S9.P3 → S9.P4 → 7)

**Key principle:** New feature changes epic integration → Must re-test entire epic

**Loop-back mechanism:**
- Similar to debugging: Fix → Loop back to testing
- Missed requirement in S9/7: Add feature → Loop back to S9.P1

---

**END OF SPECIAL CASE GUIDE**
