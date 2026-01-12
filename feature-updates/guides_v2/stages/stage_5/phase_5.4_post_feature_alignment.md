# Stage 5: Feature Implementation
## Phase 5.4: Post-Feature Alignment

**File:** `phase_5.4_post_feature_alignment.md`

**Purpose:** After completing a feature, review ALL remaining (not-yet-implemented) feature specs to ensure they align with the ACTUAL implementation (not just the plan). Update specs based on real insights from implementation to prevent spec drift and catch cascading changes early.

**Stage Flow Context:**
```
Phase 5.1 (Implementation Planning) → Phase 5.2 (Implementation) → Phase 5.3 (Post-Implementation) →
→ [YOU ARE HERE: Phase 5.4 - Cross-Feature Alignment] →
→ Phase 5.5 (Testing Plan Update) → Next Feature's Phase 5.1 (or Stage 6 if all features done)
```

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Cross-Feature Alignment, you MUST:**

1. **Use the phase transition prompt** from `prompts_reference_v2.md`
   - Find "Starting Stage 5d (Cross-Feature Alignment)" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from this guide

2. **Update README Agent Status** with:
   - Current Phase: CROSS_FEATURE_ALIGNMENT
   - Current Guide: stages/stage_5/post_feature_alignment.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "Compare to ACTUAL implementation", "Update specs proactively", "Mark features needing rework"
   - Next Action: Review feature_01 spec (first remaining feature)

3. **Verify all prerequisites** (see checklist below)

4. **THEN AND ONLY THEN** begin Cross-Feature Alignment workflow

**This is NOT optional.** Reading this guide ensures you don't miss critical spec updates.

---

## Quick Start

**What is this stage?**
Post-Feature Alignment is where you update remaining feature specs based on the just-completed feature's actual implementation, ensuring pending features align with real code patterns and integration points discovered during development.

**When do you use this guide?**
- Stage 5c complete (feature fully validated and production-ready)
- There are remaining features to implement
- Ready to align pending specs with completed work

**Key Outputs:**
- ✅ Completed feature reviewed (actual implementation understood)
- ✅ Alignment impacts identified (which specs need updates)
- ✅ Remaining feature specs updated with implementation insights
- ✅ Integration points documented
- ✅ Ready for Stage 5e (Testing Plan Update)

**Time Estimate:**
15-30 minutes per completed feature

**Exit Condition:**
Post-Feature Alignment is complete when all remaining feature specs are updated to reflect actual implementation patterns, integration points are documented, and updates are logged in each affected spec

---

## 🛑 Critical Rules

```
1. ⚠️ REVIEW ALL REMAINING FEATURES (Not just "related" ones)
   - Don't assume which features are affected
   - Implementation insights can affect unexpected features
   - Review EVERY feature that hasn't completed Stage 5c yet
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
   - Use clear criteria (see rework_criteria_examples.md)
   - If feature needs >3 new implementation tasks → return to Stage 5a
   - If spec assumptions fundamentally wrong → return to Stage 2
   - If feature should be split/removed → return to Stage 1
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
    - If any feature needs to return to Stage 2 or 1 → ask user
    - Present: What changed, why rework needed, proposed approach
    - Don't proceed with major changes without user sign-off
```

---

## Critical Decisions Summary

**Stage 5d has 1 major decision point per remaining feature:**

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
  - Return to Stage 5a (TODO creation) if >3 new tasks
  - Return to Stage 2 (Deep Dive) if spec fundamentally wrong
  - Return to Stage 1 (Epic Planning) if feature should be split/removed
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

**From Stage 5c (Post-Implementation):**
- [ ] Stage 5c completed for current feature
- [ ] All smoke tests passed
- [ ] All QC rounds passed (3 rounds)
- [ ] PR review complete
- [ ] lessons_learned.md updated
- [ ] Feature is production-ready

**Epic Structure:**
- [ ] Epic EPIC_README.md exists and is current
- [ ] At least one remaining feature exists (not yet implemented)
  - If NO remaining features → skip Stage 5d, proceed to Stage 5e then Stage 6
- [ ] All remaining features have spec.md and checklist.md files

**Agent Status:**
- [ ] README Agent Status shows Stage 5c complete
- [ ] No blockers noted
- [ ] Ready to begin alignment review

**If ANY prerequisite fails:**
- ❌ STOP - Do NOT proceed with Stage 5d
- Fix prerequisite issue first
- Update README Agent Status with blocker

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│          STAGE 5d: CROSS-FEATURE ALIGNMENT WORKFLOW          │
│                    (4 Major Steps)                            │
└──────────────────────────────────────────────────────────────┘

STEP 1: Identify Remaining Features
   ├─ List all remaining features (not yet Stage 5c complete)
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
   └─ Confirm all alignment work complete before Stage 5e
```

**See detailed workflow steps:** `stages/stage_5/alignment/alignment_workflow_steps.md`

---

## Quick Navigation

**📖 Detailed Workflow Steps:**
`stages/stage_5/alignment/alignment_workflow_steps.md`
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

**📖 Rework Criteria & Examples:**
`stages/stage_5/alignment/rework_criteria_examples.md`
- Significant Rework Criteria Table
- Decision Tree (Stage 1 vs 2 vs 5a vs Continue)
- Real-World Examples (Interface patterns, data source issues, minor updates)
- User Communication Templates

**📖 Common Mistakes to Avoid:**
`stages/stage_5/alignment/common_mistakes.md`
- 10 Anti-Patterns with corrections
- Self-check questions
- Quick reference for avoiding pitfalls

---

## Completion Criteria

**Stage 5d is complete when ALL of the following are true:**

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
- [ ] User approval obtained for any major rework (Stage 1 or 2 returns)
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
- [ ] Shows Stage 5d completion
- [ ] Documents features reviewed (count)
- [ ] Notes features needing rework (if any)
- [ ] Next action set to "Stage 5e: Testing Plan Update"

**🔄 Re-Reading Checkpoint:**
Before declaring Stage 5d complete:
1. Re-read "Critical Rules" section at top of this guide
2. Verify you compared to ACTUAL implementation (not plan)
3. Verify you updated specs PROACTIVELY (not just noted issues)
4. Verify ALL remaining features were reviewed (not just "related" ones)
5. Update README Agent Status with completion timestamp

**If ALL boxes checked:** Ready to proceed to Stage 5e

**If ANY box unchecked:** Complete missing items before proceeding

---

## Prerequisites for Next Stage

**Before transitioning to Stage 5e (Testing Plan Update), verify:**

### Completion Verification
- [ ] All Stage 5d completion criteria met (see Completion Criteria section)
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
- [ ] Updated to reflect Stage 5d completion
- [ ] Next action set to "Read stages/stage_5/post_feature_testing_update.md"

**If ALL verified:** Ready for Stage 5e

**Stage 5e Preview:**
- Review epic_smoke_test_plan.md
- Update test scenarios based on ACTUAL implementation of just-completed feature
- Add integration points discovered during implementation
- Keep testing plan current as epic evolves

**Next step:** Read stages/stage_5/post_feature_testing_update.md and use phase transition prompt

---

## Summary

**Stage 5d ensures remaining feature specs align with implementation reality through:**

1. **Comprehensive Review** - ALL remaining features reviewed (not just "related" ones)
2. **Actual Implementation Comparison** - Compare specs to ACTUAL code (not plans)
3. **Proactive Updates** - Update specs NOW (before implementation) to reflect reality
4. **Significant Rework Identification** - Clear criteria for routing features back to appropriate stage
5. **User Approval for Major Changes** - Get sign-off before major rework

**Critical protocols:**
- Review ALL remaining features sequentially
- Compare to ACTUAL implementation (read the code)
- Update specs proactively (don't defer)
- Use clear rework criteria (Stage 1, 2, or 5a)
- Get user approval for major changes

**Success criteria:**
- All remaining features reviewed
- All needed spec updates applied
- Features needing rework properly marked and routed
- Epic documentation current
- Ready for Stage 5e (Testing Plan Update)

**Why this matters:** Plans change during implementation. Code reveals insights specs couldn't predict. Stage 5d keeps remaining features aligned with reality, preventing costly rework during implementation.

---

**END OF STAGE 5d GUIDE**
