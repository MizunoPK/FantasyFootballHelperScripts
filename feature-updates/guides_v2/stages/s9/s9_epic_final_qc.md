# S9: Epic-Level Final QC Guide (ROUTER)

🚨 **IMPORTANT: This guide has been split into focused sub-stages**

**This is a routing guide.** The complete S9 workflow is now split across four focused guides:

- **S9.P1**: Epic Smoke Testing
- **S9.P2**: Epic QC Rounds
- **S9.P3**: User Testing
- **S9.P4**: Epic Final Review

**📖 Read the appropriate sub-stage guide based on your current step.**

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Navigation](#quick-navigation)
3. [Overview](#overview)
4. [Sub-Stage Breakdown](#sub-stage-breakdown)
5. [Workflow Through Sub-Stages](#workflow-through-sub-stages)
6. [Mandatory Restart Protocol](#mandatory-restart-protocol)
7. [Critical Rules (Same Across All Sub-Stages)](#critical-rules-same-across-all-sub-stages)
8. [How to Use This Router Guide](#how-to-use-this-router-guide)
9. [Exit Criteria](#exit-criteria)
10. [Next Stage After S9](#next-stage-after-s9)
11. [Why S9 Was Split](#why-s9-was-split)
12. [Frequently Asked Questions](#frequently-asked-questions)
13. [Original Guide Location](#original-guide-location)
14. [Summary](#summary)

---

## Prerequisites

**Before starting S9:**

- [ ] ALL features completed through S8.P2 (Epic Testing Update)
- [ ] All feature-level testing passed (S7 complete for all features)
- [ ] All features committed to git branch
- [ ] epic_smoke_test_plan.md updated with latest version (from S8.P2)
- [ ] No pending bug fixes or debugging sessions
- [ ] EPIC_README.md Feature Tracking shows all features with S8.P2 checked

**If any prerequisite fails:**
- Return to incomplete features and finish S7-S8
- Do NOT start S9 until ALL features are fully complete

---

## Quick Navigation

**Use this table to find the right guide:**

| Current Phase | Guide to Read | Time Estimate |
|---------------|---------------|---------------|
| Starting S9 | `stages/s9/s9_p1_epic_smoke_testing.md` | 60-90 min |
| S9.P1: Epic Smoke Testing | `stages/s9/s9_p1_epic_smoke_testing.md` | 45-75 min |
| S9.P2: QC Rounds | `stages/s9/s9_p2_epic_qc_rounds.md` | 2-3 hours |
| S9.P3: User Testing | `stages/s9/s9_p3_user_testing.md` | Variable |
| S9.P4: Epic Final Review | `stages/s9/s9_p4_epic_final_review.md` | 1.5-2 hours |

---

## Overview

**What is S9?**
Epic-Level Final QC is where you validate the ENTIRE epic as a cohesive whole after ALL features are implemented. This includes epic smoke testing, 3 QC rounds, and epic-level PR review.

**Total Time Estimate:** 4-7 hours (9 steps across 4 guides, 1 mandatory restart protocol)

**Exit Condition:** S9 is complete when epic smoke testing passed, all 3 QC rounds passed, user testing passed (no bugs found), epic PR review passed (all 11 categories), and all issues resolved (no pending bug fixes)

---

## Sub-Stage Breakdown

### S9.P1: Epic Smoke Testing

**Read:** `stages/s9/s9_p1_epic_smoke_testing.md`

**What it covers:**
- **Step 1:** Pre-QC Verification (verify all features at S8.P2 (Epic Testing Update), no pending bug fixes)
- **Step 2:** Epic Smoke Testing (4 parts: Import, Entry Point, E2E Execution, Cross-Feature Integration)

**Key Outputs:**
- Epic smoke testing results (PASSED for all 4 parts)
- DATA VALUE verification (not just file existence)
- Cross-feature integration scenarios tested
- Documented in epic_lessons_learned.md

**Time Estimate:** 60-90 minutes

**When complete:** Transition to S9.P2

**Why this sub-stage exists:**
- Focuses on functional validation before quality checks
- 4-part smoke testing ensures epic works end-to-end
- Mandatory gate before QC rounds (must pass to proceed)

---

### S9.P2: Epic QC Rounds

**Read:** `stages/s9/s9_p2_epic_qc_rounds.md`

**What it covers:**
- **Step 3:** QC Round 1 - Cross-Feature Integration (integration points, data flow, interfaces, error propagation)
- **Step 4:** QC Round 2 - Epic Cohesion & Consistency (code style, naming, error handling, architectural patterns)
- **Step 5:** QC Round 3 - End-to-End Success Criteria (original goals, success criteria, UX flow, performance)

**Key Outputs:**
- QC Round 1 findings (integration issues identified and resolved)
- QC Round 2 findings (consistency issues identified and resolved)
- QC Round 3 validation (ALL success criteria met 100%)
- Documented in epic_lessons_learned.md

**Time Estimate:** 2-3 hours (45-60 min per round)

**When complete:** Transition to S9.P3 (User Testing)

**Why this sub-stage exists:**
- Deep validation of epic quality (not just functionality)
- 3 distinct focus areas (integration, consistency, success criteria)
- Each round has specific validation checklists
- Systematic approach to epic-level quality assurance

---

### S9.P3: User Testing

**Read:** `stages/s9/s9_p3_user_testing.md`

**What it covers:**
- **Step 6:** User Testing & Bug Fix Protocol (user tests epic with real data and workflows)

**Key Outputs:**
- User testing request presented
- User testing results received
- All user-reported bugs fixed (if any)
- Epic validated by actual user
- EPIC_README.md updated with user testing results

**Time Estimate:** Variable (depends on user availability and bug count)

**When complete:** Transition to S9.P4 (Epic Final Review)

**Why this sub-stage exists:**
- User testing catches issues automated testing misses
- Real-world validation with actual user workflows
- User perspective identifies usability problems
- Mandatory quality gate before final review

---

### S9.P4: Epic Final Review

**Read:** `stages/s9/s9_p4_epic_final_review.md`

**What it covers:**
- **Step 7:** Epic PR Review (11 Categories - Epic Scope)
- **Step 8:** Validate Against Epic Request (original user goals)
- **Step 9:** Final Verification & README Update

**Key Outputs:**
- Epic PR review results (all 11 categories PASSED)
- Bug fixes created (if issues found)
- S9 restarted after bug fixes (if applicable)
- EPIC_README.md updated (S9 complete)
- epic_lessons_learned.md updated
- Ready to proceed to S10

**Time Estimate:** 60-90 minutes (if no issues) + 2-4 hours per bug fix

**When complete:** S9 COMPLETE, ready for S10

**Why this sub-stage exists:**
- Final validation before epic completion
- 11-category PR review ensures comprehensive coverage
- Validation against original epic request
- Clear completion criteria

---

## Workflow Through Sub-Stages

```text
┌──────────────────────────────────────────────────────────────┐
│                   S9 Workflow                           │
└──────────────────────────────────────────────────────────────┘

Start Epic Final QC
          │
          ▼
    ┌─────────────┐
    │  STAGE_6a   │  Epic Smoke Testing
    │  (60-90min) │  • Step 1: Pre-QC Verification
    └─────────────┘  • Step 2: Epic Smoke Testing (4 parts)
          │
    [Smoke Testing Passed?]
          │
          ▼
    ┌─────────────┐
    │  STAGE_6b   │  Epic QC Rounds
    │  (2-3 hours)│  • Step 3: QC Round 1 (Integration)
    └─────────────┘  • Step 4: QC Round 2 (Consistency)
          │          • Step 5: QC Round 3 (Success Criteria)
          │
    [All QC Rounds Passed?]
          │
          ▼
    ┌─────────────┐
    │  STAGE_6c   │  User Testing
    │  (Variable) │  • Step 6: User Testing & Bug Fix Protocol
    └─────────────┘
          │
    [User Reports Bugs?]
     │           │
    YES         NO
     │           │
     ▼           ▼
  Bug Fix   Proceed to
  Workflow   STAGE_6d
     │           │
     ▼           │
  RESTART       │
  STAGE_6       │
  (6a→6b→6c)   │
     │           │
     └───────────┘
          │
          ▼
    ┌─────────────┐
    │  STAGE_6d   │  Epic Final Review
    │  (60-90min) │  • Step 7: Epic PR Review (11 Categories)
    └─────────────┘  • Step 8: Validate Against Epic Request
          │          • Step 9: Final Verification
          │
    [All Complete?]
          │
          ▼
      S9
      COMPLETE
          │
          ▼
      S10
```

---

## Mandatory Restart Protocol

**CRITICAL:** If ANY issues are found during S9, you MUST:

1. **Create bug fixes** using bug fix workflow (S2 → S5 → S6 → S7)
2. **RESTART S9 from STAGE_6a** (cannot partially continue)
3. **Re-run ALL steps:**
   - STAGE_6a: Epic Smoke Testing (all 4 parts)
   - STAGE_6b: QC Rounds 1, 2, 3
   - STAGE_6c: Epic PR Review (all 11 categories)
4. **Document restart** in epic_lessons_learned.md

**Why COMPLETE restart?**
- Bug fixes may have affected areas already checked
- Cannot assume previous QC results still valid
- Ensures epic-level quality maintained

**Cannot proceed to S10 without passing S9 restart.**

---

## Critical Rules (Same Across All Sub-Stages)

```text
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Apply to ALL S9 sub-stages           │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALWAYS use EVOLVED epic_smoke_test_plan.md (not original from S1)
   - Plan evolved through S4 and S8.P2 (Epic Testing Update)
   - Reflects actual implementation, not assumptions

2. ⚠️ Verify DATA VALUES, not just file existence
   - Files can exist with incorrect data
   - Check actual values in CSVs, JSONs, outputs

3. ⚠️ Epic-level validation focuses on INTEGRATION
   - Feature-level validation done in S7 (Testing & Review)
   - Focus: Cross-feature workflows, integration points, cohesion

4. ⚠️ ALL 3 QC rounds are MANDATORY (cannot skip)
   - Round 1: Integration (data flow, interfaces)
   - Round 2: Consistency (code style, patterns)
   - Round 3: Success Criteria (original goals met)

5. ⚠️ If ANY issues found → create bug fix → RESTART S9
   - No inline fixes (use bug fix workflow)
   - COMPLETE restart from STAGE_6a (not partial)

6. ⚠️ Epic PR review has 11 categories (all mandatory)
   - Architecture category (Step 6.9) is MOST IMPORTANT
   - Focus on epic-wide concerns (not feature-level)

7. ⚠️ Validate against ORIGINAL epic request (not evolved specs)
   - Re-read {epic_name}.txt file
   - Verify user's stated goals achieved

8. ⚠️ 100% test pass rate required throughout S9
   - All unit tests must pass
   - Fix ALL test failures before proceeding

9. ⚠️ Zero tolerance for epic-level quality issues
   - Architectural inconsistencies → HIGH priority bug fix
   - Performance regressions >100% → HIGH priority bug fix
   - Cross-feature errors → HIGH priority bug fix
```

---

## How to Use This Router Guide

### If you're starting S9:

**READ:** `stages/s9/s9_p1_epic_smoke_testing.md`

**Use the phase transition prompt** from `prompts_reference_v2.md`:
```markdown
I'm starting S6 (Epic Smoke Testing) for Epic: {epic_name}.

I acknowledge:
- This guide covers Steps 1-2 (Pre-QC Verification → Epic Smoke Testing)
- I must use EVOLVED epic_smoke_test_plan.md (not original from S1)
- Smoke testing has 4 mandatory parts (Import, Entry Point, E2E, Cross-Feature Integration)
- I must verify DATA VALUES (not just file existence)
- If ANY part fails → fix and restart smoke testing from Part 1

Ready to begin Step 1: Pre-QC Verification.
```

---

### If you're resuming mid-S9:

**Check EPIC_README.md Agent Status** to see current step:

```markdown
**Current Stage:** S9 - Epic Final QC
**Current Step:** Step {N} - {Description}
```

**Then read the appropriate guide:**
- **Step 1 or 2:** Read stages/s9/s9_p1_epic_smoke_testing.md
- **Step 3, 4, or 5:** Read stages/s9/s9_p2_epic_qc_rounds.md
- **Step 6:** Read stages/s9/s9_p3_user_testing.md
- **Step 7, 8, or 9:** Read stages/s9/s9_p4_epic_final_review.md

**Continue from "Next Action" in Agent Status.**

---

### If you're transitioning between sub-stages:

**After completing STAGE_6a:**
- Update EPIC_README.md Agent Status: "STAGE_6a complete, starting STAGE_6b"
- **READ:** `stages/s9/s9_p2_epic_qc_rounds.md` (full guide)
- Use phase transition prompt from `prompts_reference_v2.md`

**After completing STAGE_6b:**
- Update EPIC_README.md Agent Status: "STAGE_6b complete, starting STAGE_6c (User Testing)"
- **READ:** `stages/s9/s9_p3_user_testing.md` (full guide)
- Use phase transition prompt from `prompts_reference_v2.md`

**After completing STAGE_6c:**
- Update EPIC_README.md Agent Status: "STAGE_6c complete (User Testing PASSED), starting STAGE_6d"
- **READ:** `stages/s9/s9_p4_epic_final_review.md` (full guide)
- Use phase transition prompt from `prompts_reference_v2.md`

**After completing STAGE_6d:**
- S9 is COMPLETE
- Update EPIC_README.md Epic Progress Tracker
- Proceed to S10 (Epic Cleanup)

---

## Exit Criteria

**S9 is complete when ALL of these are true:**

□ **All 9 steps complete:**
  - Step 1: Pre-QC Verification complete
  - Step 2: Epic Smoke Testing PASSED (all 4 parts)
  - Step 3: QC Round 1 PASSED (Cross-Feature Integration)
  - Step 4: QC Round 2 PASSED (Epic Cohesion & Consistency)
  - Step 5: QC Round 3 PASSED (End-to-End Success Criteria)
  - Step 6: User Testing PASSED (user reports "No bugs found")
  - Step 7: Epic PR Review PASSED (all 11 categories)
  - Step 8: Validate Against Epic Request PASSED
  - Step 9: Final Verification complete

□ **Epic Smoke Testing:**
  - Part 1 (Import Tests): ✅ PASSED
  - Part 2 (Entry Point Tests): ✅ PASSED
  - Part 3 (E2E Execution Tests): ✅ PASSED with correct data values
  - Part 4 (Cross-Feature Integration Tests): ✅ PASSED

□ **QC Rounds:**
  - QC Round 1 (Cross-Feature Integration): ✅ PASSED
  - QC Round 2 (Epic Cohesion & Consistency): ✅ PASSED
  - QC Round 3 (End-to-End Success Criteria): ✅ PASSED (100% of criteria met)

□ **Epic PR Review:**
  - All 11 categories reviewed: ✅ PASSED
  - Architectural consistency validated: ✅ PASSED
  - No issues requiring bug fixes

□ **Documentation:**
  - epic_lessons_learned.md updated with S9 insights (all sub-stages)
  - EPIC_README.md Epic Progress Tracker shows S9 complete
  - EPIC_README.md Agent Status shows S9.P3 complete

□ **Bug Fixes (if any):**
  - All bug fixes created and completed (S7 (Testing & Review))
  - S9 RESTARTED after bug fixes (from STAGE_6a)
  - All steps re-run and passed

□ **Quality Gates:**
  - All unit tests passing (100%)
  - No pending issues
  - Original epic goals validated and achieved
  - Ready to proceed to S10

**DO NOT proceed to S10 until ALL completion criteria are met.**

---

## Next Stage After S9

**When S9 complete:**
- Transition to S10 (Epic Cleanup)

📖 **READ:** `stages/s10/s10_epic_cleanup.md`

**Use the phase transition prompt** from `prompts_reference_v2.md`

---

## Why S9 Was Split

### Problems with Original Monolithic Guide (1,644 lines):

1. **Token inefficiency:** Agents loaded entire guide even when working on single step
2. **Navigation difficulty:** Hard to find specific step content in 1,644 line document
3. **Context dilution:** Important step-specific rules buried in massive guide
4. **Checkpoint confusion:** Unclear when to re-read guide vs continue

### Benefits of Split Guides:

1. **50-70% token reduction per step:**
   - STAGE_6a: ~829 lines vs 1,644 lines (50% reduction)
   - STAGE_6b: ~1,000 lines vs 1,644 lines (39% reduction)
   - STAGE_6c: ~950 lines vs 1,644 lines (42% reduction)

2. **Clear step boundaries:**
   - Natural breakpoints at workflow transitions
   - Each guide has focused critical rules
   - Obvious transition points

3. **Improved navigation:**
   - Agents read only relevant step content
   - Faster guide comprehension
   - Easier to resume after session compaction

4. **Better mandatory reading protocol:**
   - Clear "read this guide" instruction per step
   - Step-specific acknowledgment prompts
   - Reduced guide abandonment

---

## Frequently Asked Questions

**Q: Do I need to read all three sub-stage guides?**
A: Yes, but sequentially. Read STAGE_6a first, complete it, then read STAGE_6b, complete it, then read STAGE_6c.

**Q: Can I skip a step?**
A: No. All 8 steps are mandatory. The split doesn't change workflow, just organization.

**Q: What if I'm resuming mid-stage?**
A: Check EPIC_README.md Agent Status for current step, then read the guide for that step.

**Q: What if I find issues during S9?**
A: Create bug fixes using bug fix workflow (S2 → S5 → S6 → S7), then RESTART S9 from STAGE_6a.

**Q: Can I partially continue S9 after bug fixes?**
A: No. You MUST COMPLETELY RESTART S9 from STAGE_6a (smoke testing) after ANY bug fixes.

**Q: What's the difference between feature-level testing (5c) and epic-level testing (6)?**
A: Feature-level testing (5c) validates features in ISOLATION. Epic-level testing (6) validates features working TOGETHER as a cohesive system.

**Q: Can I use the original epic_smoke_test_plan.md from S1?**
A: No. You MUST use the EVOLVED epic_smoke_test_plan.md (updated in S4 and S8.P2 (Epic Testing Update)). The original plan is outdated.

**Q: Can I reference the original guide?**
A: Yes. The original guide is backed up as `STAGE_6_epic_final_qc_guide_ORIGINAL_BACKUP.md` for reference, but use the new split guides for workflow.

---

## Original Guide Location

**Backup:** `STAGE_6_epic_final_qc_guide_ORIGINAL_BACKUP.md`

**Purpose:** Historical reference only. Do NOT use for workflow.

The original guide has been preserved for reference but is deprecated. All S9 work should use the new split guides (6a, 6b, 6c).

---

## Summary

**S9 is now split into four focused guides:**

1. **stages/s9/s9_p1_epic_smoke_testing.md** - Epic Smoke Testing (Steps 1-2)
2. **stages/s9/s9_p2_epic_qc_rounds.md** - Epic QC Rounds (Steps 3-5)
3. **stages/s9/s9_p3_user_testing.md** - User Testing (Step 6)
4. **stages/s9/s9_p4_epic_final_review.md** - Epic Final Review (Steps 7-9)

**Workflow updated:** 9 steps (added User Testing), 1 mandatory restart protocol, enhanced completion criteria

**Improvement:** 50-70% reduction in guide size per step, clearer navigation, better step focus

**Start here:** `stages/s9/s9_p1_epic_smoke_testing.md` (unless resuming mid-stage)

**Critical distinction:** Epic-level validation focuses on integration, cohesion, and cross-feature quality (NOT feature-level testing)

**Mandatory restart:** If ANY issues found → bug fix → RESTART from STAGE_6a

---

*End of stages/s9/s9_epic_final_qc.md (ROUTER)*
