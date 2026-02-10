# S8: Post-Feature Alignment
## S8.P1: Cross-Feature Spec Alignment

**File:** `s8_p1_cross_feature_alignment.md`

**Purpose:** After completing a feature, review ALL remaining (not-yet-implemented) feature specs to ensure they align with the ACTUAL implementation (not just the plan). Update specs based on real insights from implementation to prevent spec drift and catch cascading changes early.

**Stage Flow Context:**
```text
S5 (Implementation Planning) → S6 (Implementation Execution) → S7 (Testing & Review) →
→ [YOU ARE HERE: S8.P1 - Cross-Feature Alignment] →
→ S8.P2 (Testing Plan Update) → Next Feature's S5 (or S9 if all features done)
```

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Cross-Feature Alignment, you MUST:**

1. **Use the phase transition prompt** from `prompts_reference_v2.md`
   - Find "Starting S8.P1" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from this guide

2. **Update README Agent Status** with:
   - Current Phase: CROSS_FEATURE_ALIGNMENT
   - Current Guide: stages/s8/s8_p1_cross_feature_alignment.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "Compare to ACTUAL implementation", "Update specs proactively", "Mark features needing rework"
   - Next Action: Review feature_01 spec (first remaining feature)

3. **Verify all prerequisites** (see checklist below)

4. **THEN AND ONLY THEN** begin Cross-Feature Alignment workflow

**This is NOT optional.** Reading this guide ensures you don't miss critical spec updates.

---

## Overview

**What is this guide?**
Post-Feature Alignment is where you update remaining feature specs based on the just-completed feature's actual implementation, ensuring pending features align with real code patterns and integration points discovered during development.

**When do you use this guide?**
- S7 (Testing & Review) complete (feature fully validated and production-ready)
- There are remaining features to implement
- Ready to align pending specs with completed work

**Key Outputs:**
- ✅ Completed feature reviewed (actual implementation understood)
- ✅ Alignment impacts identified (which specs need updates)
- ✅ Remaining feature specs updated with implementation insights
- ✅ Integration points documented
- ✅ Ready for S8.P2

**Time Estimate:**
15-30 minutes per completed feature

**Exit Condition:**
Post-Feature Alignment is complete when all remaining feature specs are updated to reflect actual implementation patterns, integration points are documented, and updates are logged in each affected spec

---

## 🛑 Critical Rules

```text
1. ⚠️ REVIEW ALL REMAINING FEATURES (Not just "related" ones)
   - Don't assume which features are affected
   - Implementation insights can affect unexpected features
   - Review EVERY feature that hasn't completed S7 (Testing & Review) yet
   - Sequentially go through all remaining features

2. ⚠️ COMPARE TO ACTUAL IMPLEMENTATION (Not the plan)
   - Don't compare to original TODO or plan
   - Look at ACTUAL code that was written
   - Check ACTUAL interfaces created
   - Verify ACTUAL data structures used
   - Review ACTUAL integration patterns implemented

3. ⚠️ UPDATE SPECS PROACTIVELY (Don't wait for implementation)
   - If spec assumptions wrong → update NOW
   - If interface changed → update dependent specs NOW
   - If data structure different → update dependent features NOW
   - Don't defer updates to "we'll figure it out during implementation"

4. ⚠️ MARK FEATURES NEEDING SIGNIFICANT REWORK
   - Use clear criteria (see below)
   - If feature needs >3 new implementation tasks → return to S5
   - If spec assumptions fundamentally wrong → return to S2
   - If feature should be split/removed → return to S1
   - Document WHY rework needed

5. ⚠️ DOCUMENT INSIGHTS IN SPEC
   - Don't just update spec silently
   - Add "Updated based on {feature_name} implementation" note
   - Explain WHY spec changed
   - Reference actual code locations that drove update

6. ⚠️ UPDATE CHECKLIST.MD TOO
   - Don't just update spec.md
   - Update corresponding checklist.md items
   - Mark any resolved questions/decisions
   - Add new questions if implementation revealed unknowns

7. ⚠️ CHECK DEPENDENCIES (Both directions)
   - Features that DEPEND on just-completed feature (downstream)
   - Features that just-completed feature DEPENDS on (upstream)
   - Shared interfaces, data structures, configuration
   - Integration points and workflows

8. ⚠️ NO "PROBABLY FINE" ASSUMPTIONS
   - If unsure if spec needs updating → READ THE ACTUAL CODE
   - If unsure if interface changed → CHECK THE ACTUAL CLASS
   - Don't assume → verify
   - 5 minutes checking saves hours of rework

9. ⚠️ UPDATE EPIC README
   - Document alignment check completion
   - Note any features marked for rework
   - Update epic status if significant changes needed

10. ⚠️ GET USER APPROVAL FOR SIGNIFICANT REWORK
    - If any feature needs to return to S2 or 1 → ask user
    - Present: What changed, why rework needed, proposed approach
    - Don't proceed with major changes without user sign-off
```

---

## Critical Decisions Summary

**S8.P1 (Cross-Feature Alignment) has 1 major decision point per remaining feature:**

### Decision Point (Per Feature): Spec Update Classification (UPDATE/REWORK/NO CHANGE)
**Question:** After comparing spec to actual implementation, what level of change is needed?

**Classification criteria:**

**Option A: NO CHANGE**
- Spec assumptions were correct
- Actual implementation matches spec expectations
- No cascading effects from completed feature
- ✅ Mark feature as "Reviewed - No changes needed"
- Proceed to next remaining feature

**Option B: MINOR UPDATE (update spec now, continue normally)**
- Spec assumptions slightly off but fixable with spec edits
- Changes are clarifications, not fundamental shifts
- Examples: Interface signature slightly different, data structure naming changed
- **Action:** Update spec.md and checklist.md NOW with actual implementation details
- ✅ Mark feature as "Spec updated based on {completed_feature}"
- Proceed to next remaining feature

**Option C: SIGNIFICANT REWORK REQUIRED (return to earlier stage)**
- Spec assumptions fundamentally wrong
- Completed feature revealed major gaps or conflicts
- **Criteria for REWORK:**
  - >3 new implementation tasks needed
  - Core algorithm approach no longer valid
  - Data dependencies changed fundamentally
  - Feature should be split or removed
- **Action based on severity:**
  - Return to S5 (TODO creation) if >3 new tasks
  - Return to S2 (Deep Dive) if spec fundamentally wrong
  - Return to S1 (Epic Planning) if feature should be split/removed
- ❌ Mark feature as "REQUIRES REWORK - {reason}"
- Document WHY rework needed
- Get user approval before proceeding

**Impact:** Deferring spec updates to "during implementation" causes rework. Updating specs NOW based on actual implementation prevents cascading failures.

---

**Summary of Alignment Review:**
- Review ALL remaining features (not just "related" ones)
- Compare to ACTUAL implementation (not the plan)
- Classify EACH feature: NO CHANGE / MINOR UPDATE / REWORK
- Update specs proactively (don't defer to implementation)
- Get user approval for any REWORK classifications

---

## Prerequisites Checklist

**Verify these BEFORE starting Cross-Feature Alignment:**

**From S7 (Testing & Review) (Post-Implementation):**
- [ ] S7 (Testing & Review) completed for current feature
- [ ] All smoke tests passed
- [ ] S7 Validation Loop passed (3 consecutive clean rounds)
- [ ] PR review complete
- [ ] lessons_learned.md updated
- [ ] Feature is production-ready

**Epic Structure:**
- [ ] Epic EPIC_README.md exists and is current
- [ ] At least one remaining feature exists (not yet implemented)
  - If NO remaining features → skip S8.P1 (Cross-Feature Alignment), proceed to S8.P2 (Epic Testing Update) then S9
- [ ] All remaining features have spec.md and checklist.md files

**Agent Status:**
- [ ] README Agent Status shows S7 (Testing & Review) complete
- [ ] No blockers noted
- [ ] Ready to begin alignment review

**If ANY prerequisite fails:**
- ❌ STOP - Do NOT proceed with S8.P1 (Cross-Feature Alignment)
- Fix prerequisite issue first
- Update README Agent Status with blocker

---

## Workflow Overview

```text
┌──────────────────────────────────────────────────────────────┐
│          S8.P1: CROSS-FEATURE ALIGNMENT WORKFLOW              │
│                    (4 Major Steps)                            │
└──────────────────────────────────────────────────────────────┘

STEP 1: Identify Remaining Features
   ├─ List all remaining features (not yet S7 (Testing & Review) complete)
   ├─ Determine review order (dependency-based)
   └─ Create review checklist

STEP 2: For Each Remaining Feature (Sequential Review)
   ├─ Read feature spec (fresh eyes)
   ├─ Read just-completed feature's ACTUAL code
   ├─ Compare spec assumptions to actual implementation
   ├─ Identify misalignments and needed updates
   ├─ Update spec.md and checklist.md NOW
   ├─ Mark feature for rework if significant changes
   └─ Commit changes, move to next feature

STEP 3: Handle Features Needing Rework
   ├─ Review significant rework criteria
   ├─ Get user approval for major rework
   └─ Update epic documentation

STEP 4: Final Verification
   └─ Confirm all alignment work complete before S8.P2 (Epic Testing Update)
```

---

## Quick Navigation

**📖 Detailed Workflow Steps:**
- Step 1: Identify Remaining Features
- Step 2: For Each Remaining Feature (Sequential Review)
  - 2a: Read Feature Spec (Fresh Eyes)
  - 2b: Read Just-Completed Feature's Actual Code
  - 2c: Compare Spec Assumptions to Actual Implementation
  - 2d: Identify Misalignments and Needed Updates
  - 2e: Update Spec.md and Checklist.md
  - 2f: Mark Feature for Rework if Significant Changes
- Step 3: Handle Features Needing Rework
- Step 4: Final Verification
- Step 5: Alignment Validation Loop (MANDATORY)

---

## Step 5: Alignment Validation Loop (MANDATORY)

**After updating remaining feature specs, validate changes with iterative loop.**

**Goal:** Achieve 2 consecutive clean loops with ZERO issues in updated specs

**When to run:**
- After EACH feature completes implementation (S6-S7)
- After S8.P1 updates remaining feature specs

**Loop Process:**
1. Review ALL specs updated in S8.P1
2. Use focused validation perspective:
   - **Loop 1 - Alignment Checker:** Verify remaining specs align with implemented feature's patterns
   - **Loop 2 - Implementation Consistency:** Check for contradictions between specs and implementation
3. Find issues (misalignments, contradictions, missing updates)
4. Resolve ALL issues (zero tolerance standard)
5. **Exit condition:** 2 consecutive clean loops (ZERO issues found)

**Differences from S3 Validation Loop:**
- **S3:** 3 loops, ALL specs, BEFORE implementation (comprehensive)
- **S8.P1:** 2 loops, UPDATED specs, AFTER each feature (incremental)
- **Both:** Zero tolerance for issues (all severities must be resolved)

**Why this matters:**
- S8.P1 updates can introduce new inconsistencies
- Issues caught immediately instead of after all features complete
- Prevents cascading alignment problems across remaining features
- Maintains consistency throughout implementation (not just at S3)

**Time Investment:**
- 2 loops: ~15-30 minutes per feature
- Prevents downstream rework: Saves 1-2 hours

**Documentation:**
Create `S8_ALIGNMENT_VALIDATION_{feature_NN}.md` with:
- Loop 1 results (perspective, issues found, resolutions)
- Loop 2 results (should be 0 issues if Loop 1 was thorough)
- Exit confirmation: 2 consecutive clean loops achieved

**Example from KAI-7:**
After Feature 01 implementation:
- S8.P1: Updated Features 02-07 specs
- Validation Loop 1: Found 2 issues (missing error handling pattern, old logging approach)
- Resolved issues
- Validation Loop 2: 0 issues found
- Proceed to S8.P2 with confirmed alignment

---

## Exit Criteria

**S8.P1 (Cross-Feature Alignment) is complete when ALL of the following are true:**

**All Remaining Features Reviewed:**
- [ ] Every remaining feature reviewed against actual implementation
- [ ] No features skipped or deferred
- [ ] Review checklist shows all features complete

**Spec Updates Applied:**
- [ ] All identified misalignments documented
- [ ] All needed spec.md updates applied
- [ ] All needed checklist.md updates applied
- [ ] Update notes include "[UPDATED based on {feature_name}]" markers
- [ ] All spec updates committed to git (one commit per feature)

**Features Needing Rework Handled:**
- [ ] Significant rework criteria applied consistently
- [ ] Features marked for rework have clear markers in spec.md
- [ ] User approval obtained for any major rework (S1 or 2 returns)
- [ ] Epic README updated with rework status
- [ ] Rework routing decisions documented (which stage to return to)

**Epic Documentation Updated:**
- [ ] EPIC_README.md reflects current status
- [ ] Epic checklist shows any features needing rework
- [ ] "Features Needing Rework" section exists if applicable
- [ ] Next steps are clear for all features

**Git History Clean:**
- [ ] All spec/checklist updates committed
- [ ] Commit messages describe alignment updates
- [ ] Working directory clean

**README Agent Status Updated:**
- [ ] Shows S8.P1 (Cross-Feature Alignment) completion
- [ ] Documents features reviewed (count)
- [ ] Notes features needing rework (if any)
- [ ] Next action set to "S8.P2 (Epic Testing Update): Testing Plan Update"

## 🛑 MANDATORY CHECKPOINT 1

**You are about to declare S8.P1 complete**

⚠️ STOP - DO NOT PROCEED TO S8.P2 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Critical Rules" section at top of this guide
2. [ ] Verify you compared to ACTUAL implementation (not implementation_plan.md)
3. [ ] Verify you updated specs PROACTIVELY (not just noted issues)
4. [ ] Verify ALL remaining features were reviewed (not just "related" ones)
5. [ ] Update EPIC_README.md Agent Status:
   - Current Guide: "stages/s8/s8_p2_epic_testing_update.md"
   - Current Step: "S8.P1 complete, ready to start S8.P2"
   - Last Updated: [timestamp]
6. [ ] Output acknowledgment: "✅ CHECKPOINT 1 COMPLETE: Re-read Critical Rules, verified actual implementation compared, all features reviewed"

**Why this checkpoint exists:**
- 80% of agents compare to implementation_plan.md instead of actual code
- Comparing to plans misses 90% of implementation deviations
- Missing proactive updates causes misaligned specs in later features

**ONLY after completing ALL 6 actions above, proceed to next section**

**If ALL boxes checked:** Ready to proceed to S8.P2 (Epic Testing Update)

**If ANY box unchecked:** Complete missing items before proceeding

---

## Prerequisites for Next Stage

**Before transitioning to S8.P2, verify:**

### Completion Verification
- [ ] All S8.P1 (Cross-Feature Alignment) completion criteria met (see Completion Criteria section)
- [ ] All remaining features reviewed
- [ ] All needed spec updates applied
- [ ] Features needing rework properly marked
- [ ] User approval obtained for major rework

### Files Updated
- [ ] All affected spec.md files updated
- [ ] All affected checklist.md files updated
- [ ] EPIC_README.md updated with current status
- [ ] Git commits describe alignment updates

### Documentation Clear
- [ ] "Features Needing Rework" section exists (if applicable)
- [ ] Next steps clear for all features
- [ ] Update notes include reasons and references

### README Agent Status
- [ ] Updated to reflect S8.P1 (Cross-Feature Alignment) completion
- [ ] Next action set to "Read stages/s8/s8_p2_epic_testing_update.md"

**If ALL verified:** Ready for S8.P2 (Epic Testing Update)

**S8.P2 (Epic Testing Update) Preview:**
- Review epic_smoke_test_plan.md
- Update test scenarios based on ACTUAL implementation of just-completed feature
- Add integration points discovered during implementation
- Keep testing plan current as epic evolves

**Next step:** Read stages/s8/s8_p2_epic_testing_update.md and use phase transition prompt

---

## Summary

**S8.P1 (Cross-Feature Alignment) ensures remaining feature specs align with implementation reality through:**

1. **Comprehensive Review** - ALL remaining features reviewed (not just "related" ones)
2. **Actual Implementation Comparison** - Compare specs to ACTUAL code (not plans)
3. **Proactive Updates** - Update specs NOW (before implementation) to reflect reality
4. **Significant Rework Identification** - Clear criteria for routing features back to appropriate stage
5. **User Approval for Major Changes** - Get sign-off before major rework

**Critical protocols:**
- Review ALL remaining features sequentially
- Compare to ACTUAL implementation (read the code)
- Update specs proactively (don't defer)
- Use clear rework criteria (S1, 2, or 5a)
- Get user approval for major changes

**Success criteria:**
- All remaining features reviewed
- All needed spec updates applied
- Features needing rework properly marked and routed
- Epic documentation current
- Ready for S8.P2

**Why this matters:** Plans change during implementation. Code reveals insights specs couldn't predict. S8.P1 (Cross-Feature Alignment) keeps remaining features aligned with reality, preventing costly rework during implementation.

---

**END OF S8.P1 GUIDE**
