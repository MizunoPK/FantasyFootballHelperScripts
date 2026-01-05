# STEP 6: User Testing & Bug Fix Protocol

**Purpose:** Have the user test the complete epic after QC rounds pass to catch real-world issues before final review and commit.

**Stage Flow Context:**
```
Stage 6a (Epic Smoke) → Stage 6b (QC Rounds 1-3) →
→ [YOU ARE HERE: Step 6 - User Testing] →
→ Step 7 (Epic PR Review) → Step 8 (Validate Epic Request) → Step 9 (Final Verification)
```

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

## Quick Start

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

```
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

4. ⚠️ RESTART STAGE 6 AFTER BUG FIXES
   - After fixing user-reported bugs → RESTART Stage 6a
   - Re-run smoke testing (4 parts)
   - Re-run QC rounds (3 rounds)
   - Re-run user testing
   - Repeat until user reports "No bugs found"

5. ⚠️ DOCUMENT USER TESTING RESULTS
   - Update EPIC_README.md with results
   - Document what user tested
   - Document user's feedback
   - Track bug fixes (if any)
```

---

## Workflow Overview

```
STEP 6: User Testing & Bug Fix Protocol
│
├─> 6a: Ask User to Test the System
│   └─ Present testing request with scenarios
│
├─> 6b: Wait for User Testing Results
│   ├─ User reports "No bugs found" → Proceed to Step 7
│   └─ User reports bugs → Follow bug fix protocol (6c)
│
├─> 6c: Bug Fix Protocol (If User Found Bugs)
│   ├─ Phase 1: Document Bugs
│   ├─ Phase 2: Fix ALL Bugs
│   ├─ Phase 3: RESTART Stage 6a (Epic Smoke Testing)
│   ├─ Phase 4: Return to Step 6 (User Testing Again)
│   └─ Repeat until user reports "No bugs found"
│
└─> 6d: Document User Testing Completion
    └─ Update EPIC_README.md with results
```

---

## Step 6a: Ask User to Test the System

**Objective:** Request that the user test the complete epic with real data and realistic workflows.

**Actions:**

Present the following request to the user:

```
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

## Step 6b: Wait for User Testing Results

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

## Step 6c: Bug Fix Protocol (If User Found Bugs)

**Triggered When:** User reports ANY bugs during testing

**Objective:** Fix ALL user-reported bugs and re-validate the epic

---

### Phase 1: Document Bugs

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
**Reported By:** User (during Stage 6 user testing)
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

```
I've documented the bugs you reported. Please verify these descriptions are accurate:

- Bug 1: {bugfix_high_data_corruption/notes.txt summary}
- Bug 2: {bugfix_medium_wrong_calculation/notes.txt summary}

Are these descriptions correct? Any clarifications needed?
```

**Wait for user confirmation before proceeding.**

---

### Phase 2: Fix ALL Bugs

For EACH bug fix folder:

**2a. Follow Bug Fix Workflow**

Read and follow: `stages/stage_5/bugfix_workflow.md`

**Stages:**
1. **Stage 2** (Feature Deep Dive) - Understand bug scope
2. **Stage 5a** (TODO Creation) - Plan fix
3. **Stage 5b** (Implementation) - Implement fix
4. **Stage 5c** (Post-Implementation) - Test fix

**2b. Mark Bug Fix Complete**

Update EPIC_README.md:

```markdown
## Bug Fixes

### Bug Fix 1: {name}
- **Priority:** high
- **Status:** Stage 5c COMPLETE ✅
- **Date Completed:** {YYYY-MM-DD}
- **Related Features:** Feature 01, Feature 03
- **Files Modified:** {list}
- **Tests Added:** {count}

### Bug Fix 2: {name}
{Details...}
```

**Repeat for ALL bugs until every bug fix reaches Stage 5c.**

---

### Phase 3: RESTART Stage 6 (Epic Final QC)

⚠️ **CRITICAL:** After ALL bugs are fixed, you MUST restart the entire Stage 6 process.

**Why restart Stage 6?**
- Bug fixes may have introduced new issues
- Need to re-validate epic integration
- QC rounds ensure fixes don't break anything
- Comprehensive validation required

**Steps to restart Stage 6:**

**3a. Return to Stage 6a (Epic Smoke Testing)**
1. Read `stages/stage_6/epic_smoke_testing.md` again
2. Execute all 4 smoke test parts:
   - Part 1: Import Test
   - Part 2: Entry Point Test
   - Part 3: E2E Execution Test
   - Part 4: Cross-Feature Integration Test
3. Verify all parts PASS

**3b. Proceed to Stage 6b (Epic QC Rounds)**
1. Read `stages/stage_6/epic_qc_rounds.md` again
2. Execute all 3 QC rounds:
   - Round 1: Cross-Feature Integration
   - Round 2: Epic Cohesion & Consistency
   - Round 3: End-to-End Success Criteria
3. Verify all rounds PASS

**3c. If Stage 6 finds MORE bugs:**
- Create new bug fix folders
- Follow bug fix protocol again
- RESTART Stage 6 AGAIN after fixes
- Repeat until Stage 6 passes with ZERO issues

**3d. Proceed to Step 6 (User Testing Again)**
- Return to this guide (Step 6)
- Ask user to test again
- Continue from Phase 4

---

### Phase 4: Return to Step 6 (User Testing Again)

**After Stage 6a and 6b pass (no bugs found during smoke/QC):**

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

### Stage 6: Epic-Level Final QC

**Stage 6a - Epic Smoke Testing:** ✅ COMPLETE
- Date completed: {YYYY-MM-DD}
- Results: All 4 parts passed

**Stage 6b - Epic QC Rounds:** ✅ COMPLETE
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
## Stage 6 Lessons Learned (Epic Final QC)

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

3. **Loop back to Stage 6a:**
   - After ALL issues resolved
   - RESTART epic smoke testing from beginning
   - Proceed through Stage 6a → 6b → Step 6 again

**Why loop back to Stage 6a (not Step 6)?**
- Bug fixes might affect epic-level integration
- Must re-validate entire epic before returning to user
- Comprehensive validation prevents new issues

---

## Next Steps

**If user testing PASSED (no bugs found):**
- ✅ Update EPIC_README.md with completion
- ✅ Update epic_lessons_learned.md
- ✅ Update Agent Status: "User Testing COMPLETE"
- ✅ Proceed to **Step 7: Epic PR Review**

**If user testing FAILED (bugs found):**
- ❌ Follow bug fix protocol (Phase 1-4)
- ❌ RESTART Stage 6a after bug fixes
- ❌ Return to Step 6 for re-testing
- ❌ Repeat until user reports "No bugs found"

---

## Summary

**User Testing Process:**

1. ✅ Ask user to test the system (Step 6a)
2. ✅ Wait for user testing results (Step 6b)
3. ✅ If bugs found → Fix all bugs → RESTART Stage 6 → Return to Step 6 (Step 6c)
4. ✅ If no bugs → Document completion → Proceed to Step 7 (Step 6d)

**Critical Requirements:**
- User testing is MANDATORY (cannot skip)
- Must wait for user response (cannot proceed without)
- ALL bugs must be fixed (cannot defer)
- Must RESTART Stage 6 after bug fixes (cannot skip validation)
- Repeat until user reports "No bugs found" (no shortcuts)

**Why this matters:**
- User testing catches issues agents miss
- Real-world validation ensures epic works
- User approval builds confidence
- Final quality gate before commit

---

*End of Step 6: User Testing & Bug Fix Protocol*
