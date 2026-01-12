# SPECIAL CASE: Discovery During Epic Testing (Stage 6/7)

**Purpose:** Handle missed requirements discovered during epic testing with special restart protocol

**When to Use:** Missed requirement discovered during Stage 6 (Epic Testing) or Stage 7 (User Testing)

**Previous Phase:** PHASE 3 & 4 (Realignment) - See `missed_requirement/realignment.md`

**Next Phase:** Restart epic testing from Phase 6.1 Step 1

---

## Why This is Different

**Normal workflow (discovered during Stage 5):**
- Plan new/updated feature (Stages 2/3/4)
- Resume paused work
- Implement features in sequence
- Continue to next stage when turn comes

**Special case (discovered during Stage 6/7):**
- Plan new/updated feature (Stages 2/3/4) ← SAME
- Resume any paused work
- **Complete ALL remaining features first** ← DIFFERENT
- **Implement new/updated feature (full Stage 5)** ← DIFFERENT
- **RESTART epic testing from Phase 6.1 Step 1** ← DIFFERENT

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

```
Discovery (Phase 6.2: Epic QC Round 1)
    ↓
PHASE 1: Discovery & User Decision (normal)
    ↓
PHASE 2: Planning - Stage 2 Deep Dive (normal)
    ↓
PHASE 3 & 4: Realignment - Stage 3 & 4 (normal)
    ↓
SPECIAL: Complete ALL Remaining Features
    ↓
SPECIAL: Implement New/Updated Feature (full Stage 5)
    ↓
SPECIAL: RESTART Epic Testing from Phase 6.1 Step 1
    ↓
Phase 6.1 → 6b → 6c → Stage 7 (entire epic flow)
```

---

## Step-by-Step Process

### Step 1-3: Normal Process (PHASE 1-4)

**Follow normal missed requirement workflow:**

1. **PHASE 1:** Discovery & User Decision
   - Use `missed_requirement/discovery.md`
   - Present options to user
   - Get decision on approach
   - Document paused work (epic testing paused)

2. **PHASE 2:** Planning (Stage 2)
   - Use `missed_requirement/planning.md`
   - Create/update feature spec
   - Full Stage 2 rigor

3. **PHASE 3 & 4:** Realignment (Stage 3 & 4)
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
- feature_03 🔄 PAUSED (was implementing when entered Stage 6)
- feature_04 ◻️ NOT STARTED
- feature_05 ◻️ NOT STARTED (NEW - from missed requirement)

Actions needed:
1. Resume and complete feature_03 (Stage 5 → complete)
2. Implement feature_04 (full Stage 5)
3. Implement feature_05 (full Stage 5)
4. Then restart epic testing
```

**Complete each feature in sequence:**
- Resume feature_03 where it left off
- Run through Stage 5 (5a → 5b → 5c → 5d → 5e) for feature_03
- Implement feature_04 (full Stage 5)
- Implement feature_05 (full Stage 5)
- **ALL features must be complete before restarting epic testing**

---

### Step 5: Implement New/Updated Feature

**When new/updated feature's turn comes in sequence:**

**Run full Stage 5:**
- Stage 5a: TODO Creation (3 rounds, 28 iterations)
- Stage 5b: Implementation Execution
- Stage 5c: Post-Implementation (smoke testing, QC rounds, final review)
- Stage 5d: Cross-Feature Spec Alignment
- Stage 5e: Epic Testing Plan Reassessment

**Same rigor as all features:**
- No shortcuts
- All rounds and iterations
- 100% test pass required
- Complete documentation

---

### Step 6: RESTART Epic Testing from Phase 6.1 Step 1

**Critical: Don't resume epic testing mid-stream**

**Why restart from beginning:**
- New feature changes epic integration
- Previous test results (Stages 6a/6b) are invalid
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
- Previous epic test progress: Phase 6.2 Round 1 (discarded)
- Restarting from: Phase 6.1 Step 1 (Epic Smoke Testing)

**Next Action:** Execute epic smoke test plan with ALL 5 features
```

**Follow Stage 6 from beginning:**

**🚨 FIRST ACTION:** Use "Starting Stage 6" prompt from `prompts/stage_6_prompts.md`

**READ:** `stages/stage_6/epic_final_qc.md`

**Execute:**
1. **Phase 6.1:** Epic Smoke Testing (Part 1-4)
   - Part 1: Import Test (all features)
   - Part 2: Entry Point Test
   - Part 3: E2E Execution Test
   - Part 4: Cross-Feature Integration Test ← **Includes new feature**

2. **Phase 6.2:** Epic QC Rounds (Round 1-3)
   - Round 1: Cross-Feature Integration
   - Round 2: Epic Cohesion & Consistency
   - Round 3: End-to-End Success Criteria

3. **Phase 6.3:** Epic Final Review
   - Code review
   - Documentation review
   - Epic readiness check

4. **Stage 7:** Epic Cleanup
   - User testing ← **User tests with new feature**
   - Commit and merge
   - Archive

---

## Examples

### Example 1: Discovery During Phase 6.2 (Epic QC Round 1)

```markdown
**Context:**
- Epic: Fantasy Football Helpers
- Stage: 6b (Epic QC Round 1)
- Features complete: feature_01, feature_02, feature_03
- Features not started: feature_04
- Discovery: Missing caching layer needed for feature_02/feature_03 integration

**Workflow:**

1. **Discovery:** Present options to user
   - Option 1: Create new feature_05_caching_layer
   - Option 2: Update feature_04
   - User chooses: Create new feature (medium priority)

2. **Planning:** Stage 2/3/4
   - Create feature_05 spec
   - Align all features
   - Update epic test plan

3. **Complete remaining features:**
   - Implement feature_04 (Stage 5a → 5e)
   - Implement feature_05 (Stage 5a → 5e)

4. **Restart epic testing:**
   - Phase 6.1 Part 1 (Import Test) - all 5 features
   - Phase 6.1 Part 2 (Entry Point Test)
   - Phase 6.1 Part 3 (E2E Test)
   - Phase 6.1 Part 4 (Cross-Feature Integration) - includes caching layer
   - Phase 6.2 (QC Rounds)
   - Phase 6.3 (Final Review)
   - Stage 7 (Cleanup & User Testing)
```

---

### Example 2: Discovery During Stage 7 (User Testing)

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

2. **Planning:** Stage 2/3/4
   - Update feature_03 spec with PDF export
   - Align all features
   - Update epic test plan

3. **Complete remaining features:**
   - No remaining features
   - Re-implement feature_03 with new scope (Stage 5a → 5e)

4. **Restart epic testing:**
   - Phase 6.1 (Epic Smoke Testing) - feature_03 now includes PDF export
   - Phase 6.2 (Epic QC Rounds)
   - Phase 6.3 (Epic Final Review)
   - Stage 7 (User Testing) - user tests again with PDF export

**Note:** Even though discovered in Stage 7, loop back to Phase 6.1 (not Stage 7)
```

---

## Comparison: Normal vs Special Case

| Aspect | Normal (Stage 5) | Special (Stage 6/7) |
|--------|-----------------|---------------------|
| **Planning** | Stages 2/3/4 ✓ | Stages 2/3/4 ✓ |
| **Resume paused work** | Resume feature implementation | Not applicable (features done) |
| **Complete remaining features** | Not required | **REQUIRED - ALL features** |
| **Implement new/updated feature** | When its turn comes in sequence | **After all remaining features** |
| **Return to** | Resume where left off | **Restart Phase 6.1 Step 1** |
| **Epic testing** | Not affected (happens later) | **Completely restarted** |

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Resuming Epic Testing Mid-Stream

**Mistake:** After implementing new feature, resume Phase 6.2 Round 1 (where left off)

**Why wrong:** Previous epic test results invalid with new feature

**Correct:** Restart from Phase 6.1 Step 1

---

### ❌ Anti-Pattern 2: Skipping Remaining Features

**Mistake:** "feature_04 is small, I'll skip it and just implement the new feature"

**Why wrong:** Epic incomplete, can't proceed to epic testing

**Correct:** Complete ALL remaining features before implementing new/updated feature

---

### ❌ Anti-Pattern 3: Partial Epic Re-Testing

**Mistake:** "I'll just re-run the integration tests affected by new feature"

**Why wrong:** Missing epic-level validation, potential issues elsewhere

**Correct:** Run complete Stage 6 (6a → 6b → 6c) from beginning

---

### ❌ Anti-Pattern 4: Returning to Stage 7 After Fixes

**Mistake:** User finds bug in Stage 7 → Fix → Resume Stage 7

**Why wrong:** Fixes might affect epic integration, need epic-level validation

**Correct:** User finds bug → Fix → Restart Phase 6.1 → Stage 7

---

## Completion Criteria

**Special case workflow complete when:**

**Planning:**
- [x] PHASE 1-4 complete (normal workflow)
- [x] New/updated feature spec created
- [x] All features aligned
- [x] Epic test plan updated

**Feature Completion:**
- [x] ALL remaining features completed (full Stage 5 each)
- [x] New/updated feature implemented (full Stage 5)
- [x] All features passing tests (100%)
- [x] Epic Progress Tracker shows all features complete

**Epic Testing Restart:**
- [x] Phase 6.1 complete (Epic Smoke Testing with new feature)
- [x] Phase 6.2 complete (Epic QC Rounds)
- [x] Phase 6.3 complete (Epic Final Review)
- [x] Ready for Stage 7 (User Testing with new feature)

---

## Summary

**Special case for Stage 6/7 discovery:**

1. Follow normal PHASE 1-4 (discovery, planning, realignment)
2. **Different:** Complete ALL remaining features first
3. **Different:** Implement new/updated feature (full Stage 5)
4. **Different:** RESTART epic testing from Phase 6.1 Step 1
5. Run complete epic testing flow (6a → 6b → 6c → 7)

**Key principle:** New feature changes epic integration → Must re-test entire epic

**Loop-back mechanism:**
- Similar to debugging: Fix → Loop back to testing
- Missed requirement in Stage 6/7: Add feature → Loop back to Phase 6.1

---

**END OF SPECIAL CASE GUIDE**
