# S9: Epic-Level Final QC
## S9.P3: User Testing & Bug Fix Protocol

**Purpose:** Have the user test the complete epic after QC rounds pass to catch real-world issues before final review and commit.

**File:** `s9_p3_user_testing.md`

**Stage Flow Context:**
```text
S9.P1 (Epic Smoke) → S9.P2 (Epic QC Validation Loop) →
→ [YOU ARE HERE: S9.P3 - User Testing] →
→ S9.P4 (Epic Final Review) → S10
```

---

## Table of Contents

1. [🚨 MANDATORY READING PROTOCOL](#-mandatory-reading-protocol)
2. [Prerequisites](#prerequisites)
3. [Overview](#overview)
4. [🛑 Critical Rules](#-critical-rules)
5. [Workflow Overview](#workflow-overview)
6. [Step S9.P1: Ask User to Test the System](#step-s9p1-ask-user-to-test-the-system)
7. [Step S9.P2: Wait for User Testing Results](#step-s9p2-wait-for-user-testing-results)
8. [Step S9.P3: Bug Fix Protocol (If User Found Bugs)](#step-s9p3-bug-fix-protocol-if-user-found-bugs)
9. [Step 6d: Document User Testing Completion](#step-6d-document-user-testing-completion)
10. [Why User Testing is Critical](#why-user-testing-is-critical)
11. [Integration with Debugging Protocol](#integration-with-debugging-protocol)
12. [Exit Criteria](#exit-criteria)
13. [Next Steps](#next-steps)
14. [Summary](#summary)

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting User Testing, you MUST:**

1. **Verify Prerequisites:**
   - Epic QC Rounds (Steps 3-5) COMPLETE
   - All 3 rounds PASSED
   - EPIC_README.md shows "Epic QC Rounds: ✅ COMPLETE"

2. **This is a MANDATORY GATE**
   - You CANNOT skip user testing
   - Epic must be tested by the actual user
   - User approval required before proceeding to PR review

---

## Prerequisites

**Before starting S9.P3 (User Testing):**

- [ ] S9.P1 complete (Epic Smoke Testing passed all 4 parts)
- [ ] S9.P2 complete (Validation loop achieved 3 consecutive clean rounds)
- [ ] EPIC_README.md shows "S9.P2: COMPLETE (3 consecutive clean rounds)"
- [ ] All features tested and validated
- [ ] No pending bug fixes or debugging sessions
- [ ] Epic is ready for end-user testing

**If any prerequisite fails:**
- Return to incomplete phase (S9.P1 or S9.P2)
- Do NOT proceed to user testing until all QC complete

---

## Overview

**What is this step?**
User Testing is where the actual user tests the complete epic with real data and realistic workflows to catch issues that automated testing and agent QC might miss.

**When do you use this step?**
- After Epic QC Rounds (Steps 3-5) complete
- All 3 QC rounds PASSED
- Before Epic PR Review (Step 7)

**Key Outputs:**
- ✅ User testing request presented to user
- ✅ User testing results received (either "No bugs" or bug list)
- ✅ All user-reported bugs fixed (if any)
- ✅ Epic validated by actual user before final review
- ✅ EPIC_README.md updated with user testing results

**Time Estimate:**
- User testing request: 5-10 minutes
- User testing time: Variable (depends on epic scope)
- Bug fixing (if needed): Variable

**Exit Condition:**
User testing passes with ZERO bugs reported by user

---

## 🛑 Critical Rules

```text
1. ⚠️ USER TESTING IS MANDATORY
   - Cannot skip this step
   - Cannot proceed to PR review without user approval
   - User must actually test (not just approve plan)
   - User tests with REAL data and realistic workflows

2. ⚠️ WAIT FOR USER RESPONSE
   - Do NOT proceed until user responds
   - User response must be explicit:
     - "No bugs found" → Proceed to Step 7
     - List of bugs → Follow bug fix protocol

3. ⚠️ ALL BUGS MUST BE FIXED
   - Cannot defer bugs to "later"
   - Cannot mark bugs as "acceptable"
   - Fix ALL bugs user reports

4. ⚠️ RESTART S9.P1 AFTER BUG FIXES
   - After fixing user-reported bugs → RESTART from S9.P1 (not S9.P2)
   - Re-run smoke testing (4 parts)
   - Re-run validation loop (until 3 consecutive clean rounds)
   - Re-run user testing
   - Repeat until user reports "No bugs found"
   - Note: This is different from S9.P2 which uses fix-and-continue

5. ⚠️ DOCUMENT USER TESTING RESULTS
   - Update EPIC_README.md with results
   - Document what user tested
   - Document user's feedback
   - Track bug fixes (if any)
```

---

## Workflow Overview

```text
STEP 6: User Testing & Bug Fix Protocol
│
├─> S9.P1: Ask User to Test the System
│   └─ Present testing request with scenarios
│
├─> S9.P2: Wait for User Testing Results
│   ├─ User reports "No bugs found" → Proceed to Step 7
│   └─ User reports bugs → Follow bug fix protocol (6c)
│
├─> S9.P3: Bug Fix Protocol (If User Found Bugs)
│   ├─ Phase 1: Document Bugs
│   ├─ Phase 2: Fix ALL Bugs
│   ├─ Phase 3: RESTART S9.P1 (Epic Smoke Testing)
│   ├─ Phase 4: Return to Step 6 (User Testing Again)
│   └─ Repeat until user reports "No bugs found"
│
└─> 6d: Document User Testing Completion
    └─ Update EPIC_README.md with results
```

---

## Step S9.P1: Ask User to Test the System

**Objective:** Request that the user test the complete epic with real data and realistic workflows.

**Actions:**

Present the following request to the user:

```markdown
Epic QC rounds have completed successfully! Before finalizing this epic, I need you to test the complete system.

**REQUEST: Please test the complete system yourself**

**What to test:**
1. Run the main application(s) affected by this epic
2. Exercise all features implemented in this epic:
   - Feature 01: {feature_name} - {brief description of what to test}
   - Feature 02: {feature_name} - {brief description of what to test}
   - Feature 03: {feature_name} - {brief description of what to test}
3. Try realistic workflows that combine multiple features
4. Test edge cases and boundary conditions
5. Verify data outputs are correct (not just structure)

**How to test:**
- Use REAL data (not test fixtures)
- Follow the epic_smoke_test_plan.md scenarios
- Try workflows you would actually use
- Look for unexpected behavior or errors
- Test with realistic data volumes
- Try edge cases you care about

**Testing scenarios to prioritize:**
{List 3-5 key scenarios from epic_smoke_test_plan.md}

**Please test the system and report:**
- "No bugs found" - if everything works correctly
- OR: List of bugs/issues discovered (one per line with description)

I'll wait for your testing results before proceeding to the final review.
```

**Customization:**
- Replace `{feature_name}` and `{description}` with actual feature details
- Extract key scenarios from epic_smoke_test_plan.md
- Include any specific edge cases user should test

---

## Step S9.P2: Wait for User Testing Results

**Objective:** Wait for user to complete testing and report results.

**DO NOT PROCEED** until user responds with testing results.

**Possible outcomes:**

### Outcome 1: User reports "No bugs found"

✅ **SUCCESS** - User testing PASSED

**Actions:**
1. Proceed to Step 6d (Document Completion)
2. Update EPIC_README.md
3. Proceed to Step 7 (Epic PR Review)

---

### Outcome 2: User reports bugs/issues

⚠️ **BUGS FOUND** - Follow bug fix protocol

**Actions:**
1. STOP current workflow
2. Proceed to Step 6c (Bug Fix Protocol)
3. Do NOT proceed to PR review until bugs fixed

---

## Step S9.P3: Bug Fix Protocol (If User Found Bugs)

**Triggered When:** User reports ANY bugs during testing

**Objective:** Fix ALL user-reported bugs and re-validate the epic

---

### Step 1: Document Bugs

**1a. Create Bug Fix Folders**

For EACH bug reported by user, create a bug fix folder:

```bash
feature-updates/KAI-{N}-{epic_name}/bugfix_{priority}_{short_name}/
```

**Priority Determination:**
- **high**: Prevents core functionality, data corruption, crashes
- **medium**: Reduces usability, incorrect results, workflow issues
- **low**: Minor issues, cosmetic problems, edge case handling

**1b. Create notes.txt for Each Bug**

In each bugfix folder, create `notes.txt`:

```markdown
# Bug Fix: {short_name}

**Priority:** {high/medium/low}
**Reported By:** User (during S9 user testing)
**Discovered During:** Epic-level user testing
**Date Reported:** {YYYY-MM-DD}

## Bug Description

{User's description of the bug}

## Steps to Reproduce

1. {Step 1}
2. {Step 2}
3. {Step 3}

## Expected Behavior

{What should happen}

## Actual Behavior

{What actually happens}

## Impact

{How this affects the epic/user}

## Related Features

{Which features are affected}
```

**1c. User Verification**

Ask user to verify notes.txt is accurate:

```text
I've documented the bugs you reported. Please verify these descriptions are accurate:

- Bug 1: {bugfix_high_data_corruption/notes.txt summary}
- Bug 2: {bugfix_medium_wrong_calculation/notes.txt summary}

Are these descriptions correct? Any clarifications needed?
```

**Wait for user confirmation before proceeding.**

---

### Step 2: Fix ALL Bugs

For EACH bug fix folder:

**2a. Follow Bug Fix Workflow**

Read and follow: `stages/s5/s5_bugfix_workflow.md`

**Stages:**
1. **S2** (Feature Deep Dive) - Understand bug scope
2. **S5** (TODO Creation) - Plan fix
3. **S6** (Implementation) - Implement fix
4. **S7 (Testing & Review)** (Post-Implementation) - Test fix

**2b. Mark Bug Fix Complete**

Update EPIC_README.md:

```markdown
## Bug Fixes

### Bug Fix 1: {name}
- **Priority:** high
- **Status:** S7 (Testing & Review) COMPLETE ✅
- **Date Completed:** {YYYY-MM-DD}
- **Related Features:** Feature 01, Feature 03
- **Files Modified:** {list}
- **Tests Added:** {count}

### Bug Fix 2: {name}
{Details...}
```

**Repeat for ALL bugs until every bug fix reaches S7 (Testing & Review).**

---

### Step 3: RESTART S9 (Epic Final QC)

⚠️ **CRITICAL:** After ALL bugs are fixed, you MUST restart the entire S9 process.

**Why restart S9?**
- Bug fixes may have introduced new issues
- Need to re-validate epic integration
- QC rounds ensure fixes don't break anything
- Comprehensive validation required

**Steps to restart S9:**

**3a. Return to S9.P1 (Epic Smoke Testing)**
1. Read `stages/s9/s9_p1_epic_smoke_testing.md` again
2. Execute all 4 smoke test parts:
   - Part 1: Import Test
   - Part 2: Entry Point Test
   - Part 3: E2E Execution Test
   - Part 4: Cross-Feature Integration Test
3. Verify all parts PASS

**3b. Proceed to S9.P2 (Epic QC Rounds)**
1. Read `stages/s9/s9_p2_epic_qc_rounds.md` again
2. Execute all 3 QC rounds:
   - Round 1: Cross-Feature Integration
   - Round 2: Epic Cohesion & Consistency
   - Round 3: End-to-End Success Criteria
3. Verify all rounds PASS

**3c. If S9 finds MORE bugs:**
- Create new bug fix folders
- Follow bug fix protocol again
- RESTART S9 AGAIN after fixes
- Repeat until S9 passes with ZERO issues

**3d. Proceed to Step 6 (User Testing Again)**
- Return to this guide (Step 6)
- Ask user to test again
- Continue from Phase 4

---

### Step 4: Return to Step 6 (User Testing Again)

**After S9.P1 and 6b pass (no bugs found during smoke/QC):**

**4a. Return to Step 6a**
- Present user testing request again
- Ask user to verify bugs are fixed
- Include testing scenarios that triggered original bugs

**4b. Wait for User Results**
- **If user finds MORE bugs:** Repeat Phase 1-4
- **If user reports "No bugs found":** Proceed to Step 6d

**Important:** Keep repeating until user testing passes with ZERO bugs.

---

## Step 6d: Document User Testing Completion

**Triggered When:** User reports "No bugs found"

**Objective:** Document successful user testing in EPIC_README.md

**Actions:**

**Update EPIC_README.md:**

```markdown
## Epic Progress Tracker

### S9: Epic-Level Final QC

**S9.P1 - Epic Smoke Testing:** ✅ COMPLETE
- Date completed: {YYYY-MM-DD}
- Results: All 4 parts passed

**S9.P2 - Epic QC Rounds:** ✅ COMPLETE
- Date completed: {YYYY-MM-DD}
- Results: All 3 rounds passed

**Step 6 - User Testing:** ✅ COMPLETE
- Date completed: {YYYY-MM-DD}
- Testing iterations: {N} (if multiple rounds due to bug fixes)
- Bugs found and fixed: {N}
- Final result: PASSED - User reports "No bugs found"
- User feedback: {Any positive feedback or notes}
- Testing scenarios validated:
  - {Scenario 1}
  - {Scenario 2}
  - {Scenario 3}

**Step 7 - Epic PR Review:** [ ] PENDING
```

**Document in epic_lessons_learned.md:**

```markdown
## S9 Lessons Learned (Epic Final QC)

### User Testing Results

**Testing Iterations:** {N}

**User Testing Round 1:**
- Date: {YYYY-MM-DD}
- Bugs found: {N}
- Bugs fixed: {list or "None"}

**User Testing Round 2:** (if applicable)
- Date: {YYYY-MM-DD}
- Bugs found: {N}
- Result: {PASSED or more bugs}

**Final User Testing:**
- Date: {YYYY-MM-DD}
- Result: PASSED - No bugs found
- User feedback: {feedback}

**Insights:**
- {What user testing caught that QC missed}
- {User perspective that was valuable}
- {Realistic workflows tested}
```

---

## Why User Testing is Critical

**Agent testing has blind spots:**
- Agents focus on technical correctness
- May miss usability issues
- Don't test realistic user workflows
- Can't evaluate "feels right" aspects

**User perspective is unique:**
- Users test workflows they actually use
- Users notice things agents overlook
- Users have domain knowledge
- Users test with real data at real scale

**Real-world validation:**
- Real data catches issues test fixtures miss
- Real workflows reveal integration problems
- Real usage patterns expose edge cases
- Real user expectations validate UX

**Final quality gate:**
- Ensures epic truly works before commit
- Validates epic meets user needs
- Catches issues before production
- User approval builds confidence

---

## Integration with Debugging Protocol

**If bugs are found during user testing:**

User-reported bugs follow the epic debugging protocol:

1. **Add bugs to epic debugging checklist:**
   - Create `{epic_name}/debugging/ISSUES_CHECKLIST.md` (if doesn't exist)
   - Add each user-reported bug to checklist

2. **Follow debugging protocol:**
   - Read `debugging/debugging_protocol.md`
   - Work through ISSUES_CHECKLIST.md systematically
   - Resolve all issues with user confirmation

3. **Loop back to S9.P1:**
   - After ALL issues resolved
   - RESTART epic smoke testing from beginning
   - Proceed through S9.P1 → 6b → Step 6 again

**Why loop back to S9.P1 (not continue validation loop)?**
- User-reported bugs indicate real-world issues missed by agent validation
- Bug fixes might affect epic-level integration
- Must re-validate entire epic before returning to user
- Comprehensive validation prevents new issues

**Note on S9.P2 vs S9.P3 restart distinction:**
- S9.P2 (Validation Loop): Fix issues immediately, continue (no restart)
- S9.P3 (User Testing): User bugs require restart from S9.P1

---

## Exit Criteria

**S9.P3 (User Testing) is complete when ONE of these is true:**

**Option 1: User Testing Passed**
- [ ] User tested the complete epic
- [ ] User reported "NO BUGS FOUND"
- [ ] EPIC_README.md updated with user testing completion
- [ ] Ready to proceed to S9.P4 (Epic Final Review)

**Option 2: User Testing Failed, Bugs Fixed, Retested Successfully**
- [ ] User tested and reported bugs
- [ ] ALL bugs documented in debugging/ISSUES_CHECKLIST.md
- [ ] ALL bugs fixed via debugging protocol
- [ ] User confirmed all fixes
- [ ] Looped back to S9.P1 (Epic Smoke Testing)
- [ ] Completed S9.P1 → S9.P2 → S9.P3 again
- [ ] User retested and reported "NO BUGS FOUND"
- [ ] Ready to proceed to S9.P4 (Epic Final Review)

**Cannot proceed to S9.P4 if:**
- User testing not performed
- User found bugs that are not yet fixed
- User has not confirmed epic is bug-free

---

## Next Steps

**If user testing PASSED (no bugs found):**
- ✅ Update EPIC_README.md with completion
- ✅ Update epic_lessons_learned.md
- ✅ Update Agent Status: "User Testing COMPLETE"
- ✅ Proceed to **Step 7: Epic PR Review**

**If user testing FAILED (bugs found):**
- ❌ Follow bug fix protocol (Phase 1-4)
- ❌ RESTART S9.P1 after bug fixes
- ❌ Return to Step 6 for re-testing
- ❌ Repeat until user reports "No bugs found"

---

## Summary

**User Testing Process:**

1. ✅ Ask user to test the system (Step 6a)
2. ✅ Wait for user testing results (Step 6b)
3. ✅ If bugs found → Fix all bugs → RESTART S9 → Return to Step 6 (Step 6c)
4. ✅ If no bugs → Document completion → Proceed to Step 7 (Step 6d)

**Critical Requirements:**
- User testing is MANDATORY (cannot skip)
- Must wait for user response (cannot proceed without)
- ALL bugs must be fixed (cannot defer)
- Must RESTART S9 after bug fixes (cannot skip validation)
- Repeat until user reports "No bugs found" (no shortcuts)

**Why this matters:**
- User testing catches issues agents miss
- Real-world validation ensures epic works
- User approval builds confidence
- Final quality gate before commit

---

*End of Step 6: User Testing & Bug Fix Protocol*
