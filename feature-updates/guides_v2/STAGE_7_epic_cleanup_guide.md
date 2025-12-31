# STAGE 7: Epic Cleanup Guide

**Guide Version:** 2.0
**Last Updated:** 2025-12-30
**Prerequisites:** Stage 6 complete (Epic Final QC passed)
**Next Stage:** None (Epic complete - moved to done/)

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Stage 7, you MUST:**

1. **Read this ENTIRE guide** using the Read tool
2. **Use the phase transition prompt** from `prompts_reference_v2.md` ("Starting Epic Cleanup")
3. **Acknowledge critical requirements** by listing them explicitly
4. **Verify ALL prerequisites** using the checklist below
5. **Update EPIC_README.md Agent Status** to reflect Stage 7 start
6. **THEN AND ONLY THEN** begin epic cleanup

**Rationale:** Stage 7 is the FINAL stage before epic completion. This stage ensures:
- All work is committed to git
- Documentation is complete and accurate
- Epic folder is ready for archival
- Future agents can understand what was accomplished

Rushing this stage results in incomplete documentation, missing commits, or disorganized done/ folder.

---

## Quick Start

**What is Stage 7?**
Epic Cleanup is the final stage where you commit all changes, verify documentation, and move the completed epic to the done/ folder for archival.

**When do you use this guide?**
- After Stage 6 (Epic Final QC) is complete
- All features implemented and validated
- Epic ready for completion

**Key Outputs:**
- ✅ All changes committed to git with clear commit message
- ✅ Documentation verified complete (README, lessons learned, etc.)
- ✅ Epic folder moved to `feature-updates/done/{epic_name}/`
- ✅ CLAUDE.md updated if workflow changes made

**Time Estimate:**
Epic cleanup typically takes 15-30 minutes.

**Critical Success Factors:**
1. Run unit tests BEFORE committing (100% pass required)
2. Verify ALL documentation complete
3. Write clear commit message describing epic
4. Move ENTIRE epic folder to done/ (not piecemeal)
5. Update CLAUDE.md if guides were improved

---

## 🛑 Critical Rules

```
┌─────────────────────────────────────────────────────────────────┐
│ CRITICAL RULES FOR STAGE 7                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 1. ⚠️ STAGE 6 MUST BE COMPLETE                                  │
│    - Verify Epic Final QC passed                                │
│    - Verify no pending bug fixes or features                    │
│    - Verify EPIC_README.md shows Stage 6 complete               │
│                                                                  │
│ 2. ⚠️ RUN UNIT TESTS BEFORE COMMITTING (100% PASS REQUIRED)     │
│    - Execute: python tests/run_all_tests.py                     │
│    - Exit code MUST be 0 (all tests passing)                    │
│    - If ANY tests fail → Fix before committing                  │
│                                                                  │
│ 3. ⚠️ VERIFY ALL DOCUMENTATION COMPLETE                         │
│    - EPIC_README.md complete and accurate                       │
│    - epic_lessons_learned.md contains insights                  │
│    - All feature README.md files complete                       │
│    - epic_smoke_test_plan.md reflects final implementation      │
│                                                                  │
│ 4. ⚠️ USER TESTING IS MANDATORY (BEFORE COMMIT)                 │
│    - Ask user to test complete system themselves                │
│    - If bugs found → Follow bug fix protocol                    │
│    - After bug fixes → RESTART Stage 6 (Epic Final QC)          │
│    - Repeat until user testing passes with ZERO bugs            │
│    - CANNOT commit without user approval                        │
│                                                                  │
│ 5. ⚠️ COMMIT MESSAGE MUST BE CLEAR AND DESCRIPTIVE              │
│    - Format: "Complete {epic_name} epic"                        │
│    - Body: List major features and changes                      │
│    - NO generic messages like "updates" or "changes"            │
│                                                                  │
│ 6. ⚠️ MOVE ENTIRE EPIC FOLDER (NOT INDIVIDUAL FEATURES)         │
│    - Move: feature-updates/{epic}/                              │
│    - To: feature-updates/done/{epic}/                           │
│    - Keep original epic request (.txt) in root for reference    │
│                                                                  │
│ 7. ⚠️ UPDATE CLAUDE.md IF GUIDES IMPROVED                        │
│    - Check epic_lessons_learned.md for guide improvements       │
│    - Update guides_v2/ files if needed                          │
│    - Update CLAUDE.md if workflow changed                       │
│                                                                  │
│ 8. ⚠️ VERIFY EPIC IS TRULY COMPLETE                             │
│    - All features implemented                                   │
│    - All tests passing                                          │
│    - All QC passed                                              │
│    - User testing passed                                        │
│    - No pending work                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites Checklist

**Before starting Stage 7, verify:**

### Stage 6 Completion
- [ ] EPIC_README.md shows "Stage 6 - Epic Final QC: ✅ COMPLETE"
- [ ] Epic smoke testing passed (all parts)
- [ ] Epic QC rounds passed (all 3 rounds)
- [ ] Epic PR review passed (all 11 categories)
- [ ] No pending issues from Stage 6

### Feature Completion Status
- [ ] ALL features show "Stage 5e complete" in EPIC_README.md
- [ ] No features in progress
- [ ] No pending bug fixes (or all bug fixes at Stage 5c)

### Test Status
- [ ] All unit tests passing (verified recently)
- [ ] No test failures
- [ ] No skipped tests

### Documentation Status
- [ ] EPIC_README.md exists and is complete
- [ ] epic_lessons_learned.md exists with insights from all stages
- [ ] epic_smoke_test_plan.md reflects final implementation
- [ ] All feature README.md files complete

**If ANY checklist item is unchecked, STOP. Do NOT proceed to Stage 7 until all prerequisites are met.**

---

## Workflow Overview

```
STAGE 7: Epic Cleanup
│
├─> STEP 1: Pre-Cleanup Verification (Verify epic truly complete)
│   ├─ Verify Stage 6 complete
│   ├─ Verify all features complete
│   ├─ Verify no pending work
│   └─ Read epic_lessons_learned.md for guide improvements
│
├─> STEP 2: Run Unit Tests (100% pass required)
│   ├─ Execute: python tests/run_all_tests.py
│   ├─ Verify exit code 0 (all tests passing)
│   └─ If ANY tests fail → Fix and re-run
│
├─> STEP 3: Documentation Verification
│   ├─ Verify EPIC_README.md complete
│   ├─ Verify epic_lessons_learned.md contains insights
│   ├─ Verify epic_smoke_test_plan.md accurate
│   ├─ Verify all feature README.md files complete
│   └─ Update any incomplete documentation
│
├─> STEP 4: Update Guides (If Needed)
│   ├─ Review epic_lessons_learned.md "Guide Improvements Needed"
│   ├─ Update guides_v2/ files if improvements identified
│   ├─ Update CLAUDE.md if workflow changed
│   └─ Document guide updates
│
├─> STEP 5: User Testing & Bug Fix Protocol (MANDATORY GATE)
│   ├─ Ask user to test the complete system themselves
│   ├─ User reports any bugs discovered during testing
│   ├─ If bugs found → Follow bug fix protocol (Stage 2→5a→5b→5c)
│   ├─ After ALL bug fixes complete → RESTART Stage 6 (Epic Final QC)
│   └─ Return to Stage 7 only when user testing passes with ZERO bugs
│
├─> STEP 6: Final Commit
│   ├─ Review all changes with git status and git diff
│   ├─ Stage all epic-related changes
│   ├─ Create commit with clear message
│   ├─ Verify commit successful
│   └─ Push to remote (if user requests)
│
├─> STEP 7: Move Epic to done/ Folder
│   ├─ Create done/ folder if doesn't exist
│   ├─ Move entire epic folder to done/
│   ├─ Verify move successful (folder structure intact)
│   └─ Leave original epic request (.txt) in root for reference
│
└─> STEP 8: Final Verification & Completion
    ├─ Verify epic in done/ folder
    ├─ Verify original request still in root
    ├─ Verify git shows clean state
    └─ Celebrate epic completion! 🎉
```

**Critical Decision Points:**
- **After Step 2:** If tests fail → Fix issues, RESTART Step 2
- **After Step 3:** If documentation incomplete → Update docs, re-verify
- **After Step 5:** If user finds bugs → Create bug fixes, RESTART Stage 6, return to Step 5
- **After Step 6:** If commit fails → Fix issues, retry commit

---

## Detailed Workflow

### STEP 1: Pre-Cleanup Verification

**Objective:** Verify epic is truly complete and ready for cleanup.

**Actions:**

**1a. Verify Stage 6 Complete**

Read EPIC_README.md "Epic Progress Tracker" section:

```markdown
**Stage 6 - Epic Final QC:** ✅ COMPLETE
- Epic smoke testing passed: ✅
- Epic QC rounds passed: ✅
- Epic PR review passed: ✅
- End-to-end validation passed: ✅
- Date completed: 2025-12-30
```

**Verify:** Stage 6 shows ✅ COMPLETE with all sub-items checked.

**If Stage 6 NOT complete:**
- STOP Stage 7
- Return to Stage 6
- Complete Stage 6 fully
- Return to Stage 7 when Stage 6 complete

**1b. Verify All Features Complete**

Check EPIC_README.md "Epic Progress Tracker":

```markdown
| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_adp_integration | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_02_matchup_system | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_03_performance_tracker | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
```

**Verify:** ALL features show ✅ through Stage 5e.

**1c. Verify No Pending Work**

Check epic folder for any incomplete work:

```bash
ls feature-updates/{epic_name}/
```

**Look for:**
- ❌ Any feature folders without "Stage 5e complete" in README.md
- ❌ Any bugfix folders without "Stage 5c complete" in README.md
- ❌ Any folders with "IN PROGRESS" status
- ❌ Any temporary files (*.tmp, *.bak, etc.)

**If pending work found:**
- STOP Stage 7
- Complete pending work
- Return to Stage 7 when all work complete

**1d. Read epic_lessons_learned.md**

Use Read tool to load epic_lessons_learned.md:

**Look for "Guide Improvements Needed" sections:**

```markdown
## Stage 5a Lessons Learned

**Guide Improvements Needed:**
- Add example for Algorithm Traceability Matrix with complex nested algorithms
- Clarify when to use high vs medium priority for bug fixes

## Stage 6 Lessons Learned

**Guide Improvements Needed:**
- None identified - Stage 6 guide worked well
```

**Document guide improvements needed:**
- Create list of guides to update
- Note specific improvements for each guide
- Prepare to update in Step 4

---

### STEP 2: Run Unit Tests

**Objective:** Verify 100% of unit tests pass before committing changes.

**Actions:**

**2a. Execute Unit Tests**

Run the complete test suite:

```bash
python tests/run_all_tests.py
```

**Expected Output:**
```
===========================================
RUNNING ALL TESTS
===========================================

Running integration tests...
✓ test_league_helper_integration.py ... 25 tests passed

Running league_helper tests...
✓ test_AddToRosterModeManager.py ... 150 tests passed
✓ test_PlayerManager.py ... 200 tests passed
... (all test files)

===========================================
SUMMARY
===========================================
Total: 2200 tests
Passed: 2200 ✅
Failed: 0
Skipped: 0

EXIT CODE: 0 ✅ (Safe to commit)
```

**2b. Verify Exit Code**

Check the exit code:

```bash
echo $?  # On Linux/Mac
echo %ERRORLEVEL%  # On Windows
```

**Expected:** 0 (all tests passing)

**If exit code is NOT 0:**
- **STOP** - Do NOT commit
- Review test output for failures
- Fix failing tests (including pre-existing failures from other epics)
- Re-run: `python tests/run_all_tests.py`
- Only proceed when exit code = 0

**Note on Pre-Existing Test Failures:**
- Stage 7 may reveal test failures that existed BEFORE this epic started
- Example: Previous epic removed a field/class but didn't update all tests
- **It is ACCEPTABLE** to fix pre-existing tests during Stage 7
- Goal: Achieve 100% test pass rate regardless of failure source
- Document fixed pre-existing tests in epic_lessons_learned.md

**2c. Verify Test Coverage**

Ensure epic-related code is tested:

**Check for:**
- ✅ New features have unit tests
- ✅ Modified functions have tests
- ✅ Integration tests exist for cross-feature workflows
- ✅ No untested code paths

**If test coverage insufficient:**
- Add missing tests
- Re-run test suite
- Verify 100% pass rate

**Why 100% pass rate is critical:**
- Ensures epic doesn't break existing functionality
- Validates new features work correctly
- Prevents regressions
- Maintains code quality standards

---

### STEP 2b: Investigate User-Reported Anomalies (If User Notices Unexpected Behavior)

**Objective:** Verify root cause of unexpected behavior empirically, don't assume based on existing code comments.

**When to use this step:**
- User notices unexpected behavior during testing (e.g., "all players have same value")
- Existing code has warnings/comments that might explain it
- Before assuming the comment is correct, verify empirically

**Actions:**

**⚠️ CRITICAL RULE:** Do NOT assume existing code comments/warnings explain the behavior - verify empirically.

**Investigation Protocol:**

**1. Create Test Script to Verify Behavior Directly**

Don't rely on existing warnings or comments. Create a focused test script that:
- Tests against source of truth (API, database, external system)
- Compares expected vs actual behavior
- Runs multiple test cases to identify patterns

**Example: User reports "all players have same ADP value"**

Even if code has warning "ESPN returns placeholders mid-season", verify:

```python
# test_api_behavior.py
import httpx

# Test CURRENT season (where user saw issue)
response_2025 = httpx.get("https://api.espn.com/.../seasons/2025/...")
players_2025 = response_2025.json()["players"]

# Test PREVIOUS season (as control)
response_2024 = httpx.get("https://api.espn.com/.../seasons/2024/...")
players_2024 = response_2024.json()["players"]

# Compare: Does API return varied values for previous season?
adp_2025 = [p["averageDraftPosition"] for p in players_2025[:10]]
adp_2024 = [p["averageDraftPosition"] for p in players_2024[:10]]

print(f"2025 ADP values: {adp_2025}")  # All 170.0?
print(f"2024 ADP values: {adp_2024}")  # Varied values?
```

**2. Compare Expected vs Actual Behavior**

**Questions to answer:**
- Does the source system return the unexpected values?
- Is it seasonal behavior (current year vs previous year)?
- Is our code extracting correctly from the source?
- Do existing warnings/comments accurately describe the behavior?

**3. Update Documentation if Root Cause Differs from Assumptions**

If investigation reveals:
- Existing comment is **accurate**: Keep comment, note verification in investigation
- Existing comment is **inaccurate**: Update comment with correct explanation
- Existing comment is **incomplete**: Add clarifying details (e.g., month range instead of week range)

**Example Update:**

Original comment:
```python
# NOTE: ESPN stopped providing real ADP mid-season (around Week 15)
```

Updated comment (after investigation):
```python
# NOTE: ESPN only provides real ADP data during draft season (Aug-Sep)
# Outside draft season (Oct-Dec), ESPN returns placeholder value of 170.0 for all players
# This is detected and warned about in player_data_fetcher_main.py
```

**4. Document Investigation in Epic Lessons Learned**

Add investigation to epic_lessons_learned.md:

```markdown
### Lesson: Empirical Verification Over Assumptions

**What Happened:**
- User noticed [unexpected behavior]
- Existing code had warning: [warning text]
- Investigation revealed: [actual root cause]

**Investigation Method:**
- Created test script to verify [source system] directly
- Tested [current scenario] vs [control scenario]
- Confirmed root cause: [findings]

**Outcome:**
- Updated documentation to clarify [what was clarified]
- Verified our code extracts data correctly
```

**Why This Matters:**
- Code comments can become outdated
- Assumptions may be incorrect or incomplete
- Empirical verification builds confidence
- Accurate documentation helps future debugging

**When NOT to use this step:**
- User doesn't report any anomalies
- Behavior is clearly expected and well-documented
- No questions about data correctness

---

### STEP 3: Documentation Verification

**Objective:** Verify all epic documentation is complete and accurate.

**Actions:**

**3a. Verify EPIC_README.md Complete**

Read EPIC_README.md and verify all sections present:

**Required Sections:**
```markdown
# Epic: {epic_name}

## 🎯 Quick Reference Card
- Current Stage: Stage 7 - Epic Cleanup
- Stage workflow diagram
- Critical rules

## Agent Status
- Last Updated: (recent timestamp)
- Current Stage: Stage 7
- Status: IN PROGRESS

## Epic Overview
- Epic description
- Epic goals
- Epic scope

## Epic Progress Tracker
- Table showing all features at Stage 5e
- Stage 6 marked complete
- Stage 7 in progress

## Feature Summary
- List of all features with descriptions
- Dependencies between features
- Current status of each feature

## Epic-Level Files
- epic_smoke_test_plan.md
- epic_lessons_learned.md

## Workflow Checklist
- Stages 1-6 all checked ✅
- Stage 7 in progress
```

**Verify:**
- ✅ All sections present
- ✅ Information accurate and up-to-date
- ✅ No placeholder text (e.g., "TODO", "{fill in later}")
- ✅ Dates are correct
- ✅ Feature list matches actual features

**If incomplete:**
- Update missing sections
- Fix inaccurate information
- Remove placeholder text

**3b. Verify epic_lessons_learned.md Contains Insights**

Read epic_lessons_learned.md:

**Required Content:**
```markdown
# Epic Lessons Learned: {epic_name}

**Epic Overview:** {brief description}
**Date Range:** {start_date} - {end_date}
**Total Features:** {N}

---

## Stage 1 Lessons Learned
**What Went Well:** ...
**What Could Be Improved:** ...
**Guide Improvements Needed:** ...

## Stage 2 Lessons Learned (Per Feature)
### Feature 01: {name}
**What Went Well:** ...
**What Could Be Improved:** ...

... (repeat for all stages and features)

## Cross-Epic Insights
- Patterns observed across multiple features
- Systemic improvements for future epics

## Recommendations for Future Epics
1. ...
2. ...
```

**Verify:**
- ✅ Insights from ALL stages present (Stages 1-6)
- ✅ Lessons from ALL features documented
- ✅ "Guide Improvements Needed" sections present
- ✅ Cross-epic insights documented
- ✅ Recommendations actionable

**If incomplete:**
- Add missing stage insights
- Document lessons from all features
- Add cross-epic patterns
- Update guide improvement notes

**3c. Verify epic_smoke_test_plan.md Accurate**

Read epic_smoke_test_plan.md:

**Verify:**
- ✅ "Last Updated" shows recent Stage 5e update
- ✅ Update History table shows all features contributed
- ✅ Test scenarios reflect ACTUAL implementation
- ✅ Integration tests included (added during Stage 5e)
- ✅ Epic success criteria still accurate

**Example Verification:**
```markdown
**Last Updated:** Stage 5e (feature_03_performance_tracker) - 2025-12-30

## Update History
| Stage | Feature | Date | Changes Made |
|-------|---------|------|--------------|
| 1 | (initial) | 2025-12-15 | Created placeholder |
| 4 | (all features) | 2025-12-20 | Updated from deep dives |
| 5e | feature_01 | 2025-12-25 | Added ADP scenarios |
| 5e | feature_02 | 2025-12-28 | Added matchup scenarios |
| 5e | feature_03 | 2025-12-30 | Added performance scenarios |
```

**If outdated:**
- Update test plan to reflect final implementation
- Add missing test scenarios
- Update success criteria
- Update "Last Updated" timestamp

**3d. Verify All Feature README.md Files Complete**

For EACH feature folder, read README.md:

**Required Content:**
```markdown
# Feature: {feature_name}

## Feature Context
- Part of Epic: {epic_name}
- Feature Number: {N}
- Purpose: {description}
- Dependencies: {list}

## Agent Status
- Current Phase: POST_IMPLEMENTATION (COMPLETE)
- Progress: 100% complete
- Status: ✅ Stage 5e complete

## Workflow Checklist
- Stages 2-5e all checked ✅

## Files in this Feature
- spec.md: ✅ Complete
- checklist.md: ✅ All resolved
- todo.md: ✅ All tasks complete
- code_changes.md: ✅ Documents all changes
- lessons_learned.md: ✅ Contains insights
```

**Verify for EACH feature:**
- ✅ README.md exists
- ✅ All sections present
- ✅ Status shows "Stage 5e complete"
- ✅ No placeholders or TODOs
- ✅ Workflow checklist all checked

**If ANY feature README incomplete:**
- Update incomplete README files
- Verify all information accurate
- Mark features as complete

---

### STEP 4: Update Guides (If Needed)

**Objective:** Apply lessons learned to improve guides for future epics.

**Actions:**

**4a. Review Guide Improvement Notes**

From epic_lessons_learned.md, compile all "Guide Improvements Needed":

**Example:**
```markdown
Guide Improvements Identified:

1. STAGE_5aa_round1_guide.md:
   - Add example for Algorithm Traceability Matrix with nested algorithms (iteration 4)

2. STAGE_5ab_round2_guide.md:
   - Clarify edge case enumeration with complex scenarios (iteration 9)

3. STAGE_5d_post_feature_alignment_guide.md:
   - Add example showing when to mark feature for "Return to Stage 5a"

4. STAGE_6_epic_final_qc_guide.md:
   - No improvements needed
```

**4b. Update Guides (If Improvements Identified)**

For EACH guide needing updates:

**Update Process:**
1. Read current guide using Read tool
2. Identify section needing improvement
3. Add example or clarification
4. Use Edit tool to update guide
5. Document change in guide's changelog

**Example Update:**

Original guide section:
```markdown
### Iteration 12: Mock Audit

Verify all mocks match real interfaces.
```

Updated guide section:
```markdown
### Iteration 12: Mock Audit

Verify all mocks match real interfaces.

**Example (Complex Nested Mocks):**
```python
# Real interface (nested return):
def get_player_stats() -> Dict[str, Dict[str, float]]:
    return {"QB": {"avg_points": 18.5, "std_dev": 3.2}}

# Mock MUST match nested structure:
mock_stats = Mock()
mock_stats.get_player_stats.return_value = {
    "QB": {"avg_points": 18.5, "std_dev": 3.2}
}
```
```

**4c. Update CLAUDE.md (If Workflow Changed)**

If epic revealed workflow improvements:

**Check if any of these changed:**
- New stages added
- Stage dependencies changed
- Critical rules updated
- File structure changed

**If workflow changed:**
- Read CLAUDE.md
- Update "Feature Development Workflow Overview" section
- Update phase transition prompts
- Document changes

**4d. Document Guide Updates**

Create summary of guide updates:

```markdown
## Guide Updates from Epic: {epic_name}

**Date:** 2025-12-30

**Guides Updated:**

1. STAGE_5aa_round1_guide.md (v2.1)
   - Added example for Algorithm Traceability Matrix with nested algorithms (iteration 4)
   - Reason: Epic feature_02 had complex nested algorithms that weren't well-documented

2. STAGE_5ac_round3_guide.md (v2.1)
   - Added example for Mock Audit with complex nested mocks (iteration 21)
   - Reason: Epic feature_02 had complex mock scenarios that needed clarification

3. STAGE_5d_post_feature_alignment_guide.md (v2.1)
   - Added example showing "Return to Stage 5a" scenario
   - Reason: Epic feature_03 required return to 5a, good teaching example

**CLAUDE.md Updates:**
- None needed (workflow unchanged)

**Commit Message for Guide Updates:**
"Update guides based on {epic_name} lessons learned"
```

**If NO guide updates needed:**
- Document: "No guide updates required from this epic"
- Proceed to Step 5

---

### STEP 5: User Testing & Bug Fix Protocol

**Objective:** Have the user test the complete system and address any bugs they discover before final commit.

**⚠️ MANDATORY GATE:** This step is REQUIRED. You CANNOT skip user testing.

**Actions:**

**5a. Ask User to Test the System**

Present the following request to the user:

```
I've completed Stages 1-6 for the {epic_name} epic. Before finalizing and committing:

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

**What to report:**
- ANY bugs, errors, or unexpected behavior you encounter
- Issues with data quality or correctness
- Performance problems or usability issues
- Any feature that doesn't work as expected

**Please test the system and report:**
- "No bugs found" - if everything works correctly
- OR: List of bugs/issues discovered (one per line with description)

I'll wait for your testing results before proceeding with the final commit.
```

**5b. Wait for User Testing Results**

**DO NOT PROCEED** until user responds with testing results.

**Possible outcomes:**

**Outcome 1: User reports "No bugs found"**
- ✅ Proceed to Step 6 (Final Commit)
- User testing complete

**Outcome 2: User reports bugs/issues**
- ⚠️ STOP Stage 7
- Follow bug fix protocol (see Step 5c)
- Do NOT proceed to Step 6 until all bugs fixed

**5c. Bug Fix Protocol (If User Found Bugs)**

If user reports ANY bugs:

**Phase 1: Document Bugs**

For EACH bug reported by user:

1. **Create bug fix folder:**
   ```
   feature-updates/{epic_name}/bugfix_{priority}_{name}/
   ```

2. **Determine priority:**
   - **high**: Breaks core functionality, produces incorrect results, prevents usage
   - **medium**: Reduces quality but system still usable, minor incorrect results
   - **low**: Cosmetic issues, minor usability problems

3. **Create notes.txt** in bug fix folder:
   ```markdown
   # Bug: {brief description}

   **Discovered By:** User testing (Stage 7)
   **Priority:** {high/medium/low}
   **Feature Affected:** {which feature or "epic-level"}

   ## Issue Description
   {User's description of the bug}

   ## Steps to Reproduce
   1. {Step 1}
   2. {Step 2}
   3. {Step 3}

   ## Expected Behavior
   {What should happen}

   ## Actual Behavior
   {What actually happens}

   ## User Verification Required
   - [ ] User confirms this notes.txt accurately describes the bug
   ```

4. **User verifies notes.txt** (ask user to confirm bug description is accurate)

**Phase 2: Fix ALL Bugs**

For EACH bug fix:

1. **Read bug fix workflow guide:**
   ```
   guides_v2/STAGE_5_bug_fix_workflow_guide.md
   ```

2. **Follow bug fix stages:**
   - Stage 2: Deep Dive (understand root cause, create spec.md)
   - Stage 5a: TODO Creation (24 iterations)
   - Stage 5b: Implementation (fix the bug)
   - Stage 5c: Post-Implementation (smoke testing, QC rounds, PR review)

3. **Mark bug fix complete** in EPIC_README.md

4. **Repeat for all bugs** until ALL bug fixes reach Stage 5c

**Phase 3: RESTART Stage 6 (Epic Final QC)**

⚠️ **CRITICAL:** After ALL bugs are fixed, you MUST restart the entire Stage 6 process:

**Why restart Stage 6?**
- Bug fixes changed the codebase
- Integration between features may have changed
- Need to re-validate epic as a whole
- Ensures bug fixes didn't introduce new issues

**What to restart:**

1. **Read Stage 6 guide again:**
   ```
   guides_v2/STAGE_6_epic_final_qc_guide.md
   ```

2. **Execute epic smoke testing (4 parts):**
   - Part 1: Epic-level import tests
   - Part 2: Epic-level entry point tests
   - Part 3: Epic E2E execution tests
   - Part 4: Cross-feature integration tests

3. **Execute epic QC rounds (3 rounds):**
   - Round 1: Cross-Feature Integration Validation
   - Round 2: Epic Cohesion & Consistency
   - Round 3: End-to-End Success Criteria

4. **Execute epic PR review (11 categories)**

5. **Validate against original epic request**

**If Stage 6 finds MORE bugs:**
- Create new bug fixes
- Fix them following bug fix protocol
- RESTART Stage 6 AGAIN
- Repeat until Stage 6 passes with ZERO issues

**Phase 4: Return to Step 5 (User Testing Again)**

After Stage 6 passes again:

1. **Return to Step 5a** (User Testing)
2. **Ask user to test again:**
   ```
   I've fixed the bugs you reported and re-validated the epic (Stage 6).

   Bugs fixed:
   - {Bug 1 brief description}
   - {Bug 2 brief description}

   Please test the system again to verify the bugs are fixed and no new issues introduced.
   ```

3. **Wait for user testing results**

4. **If user finds MORE bugs:** Repeat Phase 1-4

5. **If user reports "No bugs found":** Proceed to Step 6 (Final Commit)

**5d. Document User Testing Completion**

Once user testing passes with ZERO bugs:

Update EPIC_README.md:

```markdown
## Stage 7 - User Testing Results

**User Testing Conducted:** {YYYY-MM-DD}
**Bugs Found:** {N}
**Bugs Fixed:** {N}
**Final User Testing Result:** ✅ NO BUGS - Approved for commit

{If bugs were found and fixed:}
**Bug Fixes Created During User Testing:**
- bugfix_{priority}_{name}/: {Brief description}
- bugfix_{priority}_{name}/: {Brief description}

**Stage 6 Re-Validation:** ✅ PASSED (after bug fixes)
```

**Why User Testing is Critical:**

- **Agent testing has blind spots:** Agents focus on technical correctness, may miss usability issues
- **User perspective is unique:** Users test realistic workflows that agents might not consider
- **Real-world validation:** User testing with real data catches issues automated tests miss
- **Final quality gate:** Ensures epic truly works before committing to codebase
- **Prevents production bugs:** Better to find bugs now than after commit

**User Testing is MANDATORY** - do NOT skip this step.

---

### STEP 6: Final Commit

**Objective:** Commit all epic changes to git with clear, descriptive message.

**Actions:**

**6a. Review All Changes**

Check git status:

```bash
git status
```

**Expected Output:**
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  modified:   league_helper/util/PlayerManager.py
  modified:   league_helper/add_to_roster_mode/AddToRosterModeManager.py
  modified:   data/league_config.json

Untracked files:
  feature-updates/improve_draft_helper/
  feature-updates/improve_draft_helper/feature_01_adp_integration/
  feature-updates/improve_draft_helper/feature_02_matchup_system/
  feature-updates/improve_draft_helper/feature_03_performance_tracker/
  feature-updates/improve_draft_helper/EPIC_README.md
  feature-updates/improve_draft_helper/epic_smoke_test_plan.md
  feature-updates/improve_draft_helper/epic_lessons_learned.md
```

**Review changes with git diff:**

```bash
git diff league_helper/util/PlayerManager.py
git diff league_helper/add_to_roster_mode/AddToRosterModeManager.py
git diff data/league_config.json
```

**Verify:**
- ✅ All changes related to epic
- ✅ No unrelated changes included
- ✅ No debugging code left in (e.g., print statements)
- ✅ No commented-out code
- ✅ No sensitive data (API keys, passwords, etc.)

**6b. Stage All Epic Changes**

Add all epic-related changes:

```bash
# Stage modified files
git add league_helper/util/PlayerManager.py
git add league_helper/add_to_roster_mode/AddToRosterModeManager.py
git add data/league_config.json

# Stage epic folder (all files)
git add feature-updates/improve_draft_helper/
```

**Verify staged changes:**

```bash
git status
```

**Expected:**
```
Changes to be committed:
  modified:   league_helper/util/PlayerManager.py
  modified:   league_helper/add_to_roster_mode/AddToRosterModeManager.py
  modified:   data/league_config.json
  new file:   feature-updates/improve_draft_helper/EPIC_README.md
  new file:   feature-updates/improve_draft_helper/epic_smoke_test_plan.md
  ... (all epic files)
```

**6c. Create Commit with Clear Message**

Create commit with descriptive message:

**Commit Message Format:**
```
Complete {epic_name} epic

Major features:
- {Feature 1 brief description}
- {Feature 2 brief description}
- {Feature 3 brief description}

Key changes:
- {File 1}: {What changed and why}
- {File 2}: {What changed and why}

Testing:
- All unit tests passing (2200/2200)
- Epic smoke testing passed
- Epic QC rounds passed (3/3)
```

**Example Commit:**

```bash
git commit -m "$(cat <<'EOF'
Complete improve_draft_helper epic

Major features:
- ADP integration: Adds market wisdom via Average Draft Position data
- Matchup system: Incorporates opponent strength into projections
- Performance tracking: Tracks player accuracy vs projections

Key changes:
- PlayerManager.py: Added calculate_adp_multiplier() method
- AddToRosterModeManager.py: Integrated matchup difficulty into scoring
- league_config.json: Added adp_weights and matchup_weights parameters

Testing:
- All unit tests passing (2200/2200)
- Epic smoke testing passed (4/4 parts)
- Epic QC rounds passed (3/3)
EOF
)"
```

**6d. Verify Commit Successful**

Check git log:

```bash
git log -1 --stat
```

**Expected Output:**
```
commit a1b2c3d4e5f6... (HEAD -> main)
Author: Your Name <your@email.com>
Date:   Mon Dec 30 15:30:00 2025

    Complete improve_draft_helper epic

    Major features:
    - ADP integration: Adds market wisdom via Average Draft Position data
    - Matchup system: Incorporates opponent strength into projections
    - Performance tracking: Tracks player accuracy vs projections

    Key changes:
    - PlayerManager.py: Added calculate_adp_multiplier() method
    - AddToRosterModeManager.py: Integrated matchup difficulty into scoring
    - league_config.json: Added adp_weights and matchup_weights parameters

    Testing:
    - All unit tests passing (2200/2200)
    - Epic smoke testing passed (4/4 parts)
    - Epic QC rounds passed (3/3)

 league_helper/util/PlayerManager.py                                  | 45 ++++++
 league_helper/add_to_roster_mode/AddToRosterModeManager.py           | 32 +++-
 data/league_config.json                                              | 12 ++
 feature-updates/improve_draft_helper/EPIC_README.md                  | 250 +++++++++++++++++++++++++++++
 ... (all epic files listed)
```

**Verify:**
- ✅ Commit message clear and descriptive
- ✅ All epic files included in commit
- ✅ File change counts reasonable

**6e. Push to Remote (If User Requests)**

**IMPORTANT:** Only push if user explicitly requests it.

If user says "push changes" or "push to remote":

```bash
git push origin main
```

**Verify push successful:**
```
Enumerating objects: 45, done.
Counting objects: 100% (45/45), done.
Delta compression using up to 8 threads
Compressing objects: 100% (30/30), done.
Writing objects: 100% (32/32), 8.5 KiB | 1.2 MiB/s, done.
Total 32 (delta 18), reused 0 (delta 0)
To github.com:user/repo.git
   e5f6g7h..a1b2c3d  main -> main
```

**If push fails:**
- Check network connection
- Verify remote configured: `git remote -v`
- Pull latest changes first: `git pull origin main`
- Resolve conflicts if any
- Retry push

---

### STEP 7: Move Epic to done/ Folder

**Objective:** Move completed epic folder to done/ for archival.

**Actions:**

**7a. Create done/ Folder (If Doesn't Exist)**

Check if done/ folder exists:

```bash
ls feature-updates/
```

**If done/ doesn't exist:**

```bash
mkdir feature-updates/done
```

**7b. Move Entire Epic Folder to done/**

Move the complete epic folder:

**Windows:**
```bash
move feature-updates\improve_draft_helper feature-updates\done\improve_draft_helper
```

**Linux/Mac:**
```bash
mv feature-updates/improve_draft_helper feature-updates/done/improve_draft_helper
```

**CRITICAL:** Move the ENTIRE folder, not individual features.

**7c. Verify Move Successful**

Check folder structure:

```bash
ls feature-updates/done/improve_draft_helper/
```

**Expected:**
```
EPIC_README.md
epic_smoke_test_plan.md
epic_lessons_learned.md
feature_01_adp_integration/
feature_02_matchup_system/
feature_03_performance_tracker/
bugfix_high_interface_mismatch/  (if bug fixes existed)
```

**Verify:**
- ✅ All features present
- ✅ All epic-level files present (README, test plan, lessons learned)
- ✅ All bug fix folders present (if any)
- ✅ No files left behind in original location

**7d. Leave Original Epic Request in Root**

**IMPORTANT:** Do NOT move the original {epic_name}.txt file.

**Why:**
- Original request stays in feature-updates/ root for reference
- Easy to find for future similar epics
- Historical record of user's original vision

**Verify:**

```bash
ls feature-updates/improve_draft_helper.txt
```

**Expected:** File still exists in root.

**Structure After Move:**
```
feature-updates/
├── improve_draft_helper.txt           ← STAYS in root
├── done/
│   └── improve_draft_helper/          ← Epic MOVED here
│       ├── EPIC_README.md
│       ├── epic_smoke_test_plan.md
│       ├── epic_lessons_learned.md
│       ├── feature_01_adp_integration/
│       ├── feature_02_matchup_system/
│       └── feature_03_performance_tracker/
└── guides_v2/                         ← Guides stay in place
```

---

### STEP 8: Final Verification & Completion

**Objective:** Verify epic cleanup complete and celebrate completion!

**Actions:**

**8a. Verify Epic in done/ Folder**

Confirm epic moved successfully:

```bash
ls feature-updates/done/
```

**Expected:**
```
improve_draft_helper/
(other completed epics...)
```

**8b. Verify Original Request Still in Root**

Confirm original request accessible:

```bash
ls feature-updates/improve_draft_helper.txt
```

**Expected:** File exists.

**8c. Verify Git Shows Clean State**

Check git status:

```bash
git status
```

**Expected:**
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  renamed:    feature-updates/improve_draft_helper -> feature-updates/done/improve_draft_helper

nothing to commit (use "git add" to track renamed folder)
```

**If folder rename not committed:**

This is OPTIONAL - the epic is complete. If user wants the folder move committed:

```bash
git add feature-updates/done/improve_draft_helper
git add -u  # Stage the deletion of old location
git commit -m "Move improve_draft_helper epic to done/"
```

**8d. Update EPIC_README.md One Final Time**

Read the epic's README in done/ folder:

```bash
# Update the README in its new location
feature-updates/done/improve_draft_helper/EPIC_README.md
```

**Update Agent Status:**
```markdown
## Agent Status

**Last Updated:** 2025-12-30 16:00
**Current Stage:** Stage 7 - Epic Cleanup
**Status:** ✅ COMPLETE

**Epic Completion Summary:**
- Start Date: 2025-12-15
- End Date: 2025-12-30
- Duration: 15 days
- Total Features: 3
- Bug Fixes Created: 1
- Final Test Pass Rate: 100% (2200/2200 tests)

**Epic Moved To:** feature-updates/done/improve_draft_helper/
**Original Request:** feature-updates/improve_draft_helper.txt

**Next Steps:** None - epic complete! 🎉
```

**8e. Celebrate Epic Completion! 🎉**

The epic is now complete!

**What was accomplished:**
- ✅ Epic planned with {N} features
- ✅ All features implemented and tested
- ✅ Epic-level integration validated
- ✅ All QC rounds passed
- ✅ Documentation complete
- ✅ Changes committed to git
- ✅ Epic archived in done/ folder

**Epic is ready for:**
- Production use
- Future maintenance
- Reference for similar epics
- Lessons applied to future work

---

## Re-Reading Checkpoints

**You MUST re-read this guide when:**

1. **After Session Compaction**
   - Conversation compacted while in Stage 7
   - Re-read to restore context
   - Check EPIC_README.md Agent Status to see which step you're on

2. **After Test Failures**
   - Unit tests failed in Step 2
   - Re-read after fixing tests
   - Remember: 100% pass rate required

3. **After Commit Failures**
   - Git commit failed in Step 5
   - Re-read commit requirements
   - Verify commit message format

4. **Before Moving Epic**
   - Before executing move command in Step 6
   - Re-read move instructions
   - Verify you're moving ENTIRE folder

5. **When Encountering Confusion**
   - Unsure about next step
   - Re-read workflow overview
   - Check current step's detailed workflow

**Re-Reading Protocol:**
1. Use Read tool to load ENTIRE guide
2. Find current step in EPIC_README.md Agent Status
3. Read "Workflow Overview" section
4. Read current step's detailed workflow
5. Proceed with renewed understanding

---

## Completion Criteria

**Stage 7 is COMPLETE when ALL of the following are true:**

### Unit Tests
- [ ] All unit tests executed: `python tests/run_all_tests.py`
- [ ] Exit code = 0 (100% pass rate)
- [ ] No test failures or skipped tests

### Documentation
- [ ] EPIC_README.md complete and accurate
- [ ] epic_lessons_learned.md contains insights from all stages
- [ ] epic_smoke_test_plan.md reflects final implementation
- [ ] All feature README.md files complete

### Guide Updates
- [ ] Reviewed epic_lessons_learned.md for guide improvements
- [ ] Updated guides_v2/ files if improvements identified
- [ ] Updated CLAUDE.md if workflow changed
- [ ] Documented all guide updates

### Git Commit
- [ ] All changes reviewed with git status and git diff
- [ ] All epic changes staged
- [ ] Commit created with clear, descriptive message
- [ ] Commit successful (verified with git log)
- [ ] Pushed to remote (if user requested)

### Epic Move
- [ ] done/ folder exists
- [ ] Entire epic folder moved to done/
- [ ] Epic folder structure intact in done/
- [ ] Original epic request (.txt) still in root

### Final Verification
- [ ] Epic visible in done/ folder
- [ ] Original request accessible in root
- [ ] Git status clean (or folder rename staged)
- [ ] EPIC_README.md updated with completion status

**Epic is COMPLETE when ALL completion criteria are met.**

---

## Common Mistakes to Avoid

**Anti-Pattern Recognition:**

### ❌ MISTAKE 1: "Committing without running unit tests"

**Why this is wrong:**
- Tests might be failing
- Epic changes might break existing functionality
- Committing broken code violates project standards

**What to do instead:**
- ✅ ALWAYS run `python tests/run_all_tests.py` first
- ✅ Verify exit code = 0
- ✅ Fix any test failures before committing

---

### ❌ MISTAKE 2: "Generic commit message like 'updates' or 'changes'"

**Why this is wrong:**
- Future agents can't understand what was done
- No context for why changes were made
- Violates commit standards

**What to do instead:**
- ✅ Use format: "Complete {epic_name} epic"
- ✅ List major features in commit body
- ✅ Document key changes with reasons
- ✅ Include testing summary

---

### ❌ MISTAKE 3: "Moving individual features instead of entire epic"

**Why this is wrong:**
- Breaks epic folder structure
- Separates related work
- Loses epic-level context (README, test plan, lessons learned)

**What to do instead:**
- ✅ Move the ENTIRE epic folder: `feature-updates/{epic}/`
- ✅ Keep all features together in done/
- ✅ Keep epic-level files with features

---

### ❌ MISTAKE 4: "Moving original epic request (.txt) to done/"

**Why this is wrong:**
- Original request is reference for future similar epics
- Harder to find in done/ folder
- Loses historical context in root

**What to do instead:**
- ✅ LEAVE original {epic_name}.txt in feature-updates/ root
- ✅ Only move the epic folder (not the request file)
- ✅ Keep request easily accessible

---

### ❌ MISTAKE 5: "Skipping documentation verification"

**Why this is wrong:**
- Incomplete documentation in done/ folder
- Future agents can't understand epic
- Lessons learned are lost

**What to do instead:**
- ✅ Verify EPIC_README.md complete
- ✅ Verify epic_lessons_learned.md has insights
- ✅ Verify all feature README.md files complete
- ✅ Update any incomplete docs before moving

---

### ❌ MISTAKE 6: "Ignoring guide improvements from lessons learned"

**Why this is wrong:**
- Misses opportunity to improve workflow
- Same issues will occur in future epics
- Wastes lessons learned effort

**What to do instead:**
- ✅ Review epic_lessons_learned.md "Guide Improvements Needed"
- ✅ Update guides based on lessons
- ✅ Update CLAUDE.md if workflow changed
- ✅ Document guide updates

---

### ❌ MISTAKE 7: "Committing debugging code or print statements"

**Why this is wrong:**
- Pollutes codebase with temporary code
- Reduces code quality
- Confuses future developers

**What to do instead:**
- ✅ Review all changes with git diff
- ✅ Remove print() statements used for debugging
- ✅ Remove commented-out code
- ✅ Remove temporary files

---

### ❌ MISTAKE 8: "Skipping Stage 7 because 'epic is done after Stage 6'"

**Why this is wrong:**
- Changes not committed to git
- Epic folder not archived
- Documentation not finalized
- Future work will be confused by incomplete cleanup

**What to do instead:**
- ✅ ALWAYS complete Stage 7
- ✅ Commit changes to git
- ✅ Move epic to done/
- ✅ Finalize all documentation

---

## Real-World Examples

### Example 1: Complete Stage 7 Workflow

**Scenario:** Completing "Improve Draft Helper" epic

**Step 1: Pre-Cleanup Verification**

```bash
# Verify Stage 6 complete
cat feature-updates/improve_draft_helper/EPIC_README.md | grep "Stage 6"
# Output: **Stage 6 - Epic Final QC:** ✅ COMPLETE
```

**Step 2: Run Unit Tests**

```bash
python tests/run_all_tests.py

# Output:
# Total: 2200 tests
# Passed: 2200 ✅
# Failed: 0
# EXIT CODE: 0 ✅
```

**Step 3: Documentation Verification**

```bash
# Check EPIC_README.md
cat feature-updates/improve_draft_helper/EPIC_README.md
# ✅ All sections present

# Check epic_lessons_learned.md
cat feature-updates/improve_draft_helper/epic_lessons_learned.md
# ✅ Insights from all stages present

# Check epic_smoke_test_plan.md
cat feature-updates/improve_draft_helper/epic_smoke_test_plan.md
# ✅ Last Updated: Stage 5e (feature_03) - 2025-12-30
```

**Step 4: Update Guides**

```markdown
# From epic_lessons_learned.md:
**Guide Improvements Needed:**
- STAGE_5aa (Round 1): Add example for nested algorithms in Iteration 4

# Update guide:
# (Edit STAGE_5aa_round1_guide.md to add example)
```

**Step 5: Final Commit**

```bash
# Review changes
git status
git diff league_helper/util/PlayerManager.py

# Stage changes
git add league_helper/util/PlayerManager.py
git add league_helper/add_to_roster_mode/AddToRosterModeManager.py
git add data/league_config.json
git add feature-updates/improve_draft_helper/

# Commit
git commit -m "$(cat <<'EOF'
Complete improve_draft_helper epic

Major features:
- ADP integration: Market wisdom via Average Draft Position
- Matchup system: Opponent strength in projections
- Performance tracking: Player accuracy vs projections

Key changes:
- PlayerManager.py: Added calculate_adp_multiplier() method
- AddToRosterModeManager.py: Integrated matchup difficulty
- league_config.json: Added adp_weights and matchup_weights

Testing:
- All unit tests passing (2200/2200)
- Epic smoke testing passed (4/4 parts)
- Epic QC rounds passed (3/3)
EOF
)"

# Verify commit
git log -1 --stat
```

**Step 6: Move Epic to done/**

```bash
# Create done/ folder (if needed)
mkdir -p feature-updates/done

# Move epic folder
mv feature-updates/improve_draft_helper feature-updates/done/improve_draft_helper

# Verify move
ls feature-updates/done/improve_draft_helper/
# Output: EPIC_README.md, epic_smoke_test_plan.md, feature_01/, feature_02/, feature_03/

# Verify original request still in root
ls feature-updates/improve_draft_helper.txt
# Output: feature-updates/improve_draft_helper.txt (still exists)
```

**Step 7: Final Verification**

```bash
# Verify epic in done/
ls feature-updates/done/
# Output: improve_draft_helper/

# Verify git status
git status
# Output: renamed: feature-updates/improve_draft_helper -> feature-updates/done/improve_draft_helper

# Update EPIC_README.md in done/ folder
# (Edit to add completion summary)
```

**Epic Complete! 🎉**

---

## README Agent Status Update Requirements

**Update EPIC_README.md Agent Status section at these checkpoints:**

### Checkpoint 1: Starting Stage 7
```markdown
**Current Stage:** Stage 7 - Epic Cleanup
**Status:** IN PROGRESS
**Current Step:** Pre-Cleanup Verification
**Last Updated:** 2025-12-30 15:00
**Next Action:** Run unit tests to verify 100% pass rate
```

### Checkpoint 2: After Unit Tests
```markdown
**Current Stage:** Stage 7 - Epic Cleanup
**Status:** IN PROGRESS
**Current Step:** Documentation Verification
**Last Updated:** 2025-12-30 15:15
**Progress:** Unit tests ✅ PASSED (2200/2200)
**Next Action:** Verify all epic documentation complete
```

### Checkpoint 3: After Documentation Verification
```markdown
**Current Stage:** Stage 7 - Epic Cleanup
**Status:** IN PROGRESS
**Current Step:** Final Commit
**Last Updated:** 2025-12-30 15:30
**Progress:**
- Unit tests ✅ PASSED
- Documentation ✅ VERIFIED
**Next Action:** Commit all epic changes to git
```

### Checkpoint 4: After Commit
```markdown
**Current Stage:** Stage 7 - Epic Cleanup
**Status:** IN PROGRESS
**Current Step:** Move Epic to done/
**Last Updated:** 2025-12-30 15:45
**Progress:**
- Unit tests ✅ PASSED
- Documentation ✅ VERIFIED
- Git commit ✅ COMPLETE
**Next Action:** Move epic folder to done/
```

### Checkpoint 5: Epic Complete
```markdown
**Current Stage:** Stage 7 - Epic Cleanup
**Status:** ✅ COMPLETE
**Completed:** 2025-12-30 16:00

**Epic Completion Summary:**
- Start Date: 2025-12-15
- End Date: 2025-12-30
- Duration: 15 days
- Total Features: 3
- Bug Fixes Created: 1
- Final Test Pass Rate: 100% (2200/2200)

**Epic Location:** feature-updates/done/improve_draft_helper/
**Original Request:** feature-updates/improve_draft_helper.txt

**Next Steps:** None - epic complete! 🎉
```

---

## Prerequisites for Next Stage

**There is NO next stage after Stage 7.**

**Epic is complete when Stage 7 finishes.**

**Future work on this epic:**
- For bug fixes: Create new bug fix epic
- For enhancements: Create new enhancement epic
- For refactoring: Create new refactoring epic

**The completed epic serves as:**
- Reference implementation for similar epics
- Source of lessons learned (epic_lessons_learned.md)
- Historical record of what was accomplished
- Codebase foundation for future work

---

## Summary

**Stage 7 - Epic Cleanup finalizes the epic and archives it for future reference:**

**Key Activities:**
1. Run unit tests (100% pass required)
2. Verify all documentation complete
3. Update guides based on lessons learned
4. Commit all changes to git with clear message
5. Move entire epic folder to done/
6. Leave original epic request in root for reference
7. Celebrate epic completion! 🎉

**Critical Success Factors:**
- 100% test pass rate before committing
- Complete documentation (README, lessons learned, test plan)
- Clear, descriptive commit message
- Entire epic folder moved (not individual features)
- Guide updates applied (if lessons identified)

**Common Pitfalls:**
- Committing without running tests
- Generic commit messages
- Moving features individually instead of entire epic
- Moving original request file (should stay in root)
- Skipping documentation verification
- Ignoring guide improvements

**Epic Complete When:**
- All tests passing (100%)
- All documentation complete
- Changes committed to git
- Epic moved to done/
- Original request still in root
- EPIC_README.md shows completion status

**What Happens Next:**
- Epic is complete and archived
- Can be referenced for future similar epics
- Lessons learned applied to guide improvements
- Codebase ready for production use

**Remember:** Stage 7 is the final stage. Don't rush it - proper cleanup ensures the epic's value is preserved for future work.

---

**END OF STAGE 7 GUIDE**

---

**🎉 CONGRATULATIONS! 🎉**

**If you've reached the end of Stage 7, you've successfully completed an entire epic from start to finish:**

**What you accomplished:**
- ✅ Planned epic with feature breakdown (Stage 1)
- ✅ Deep dived into each feature (Stage 2)
- ✅ Ensured cross-feature alignment (Stage 3)
- ✅ Created epic testing strategy (Stage 4)
- ✅ Implemented all features with rigorous QC (Stage 5)
- ✅ Validated epic end-to-end (Stage 6)
- ✅ Cleaned up and archived epic (Stage 7)

**The epic is now:**
- Production-ready
- Fully tested (100% pass rate)
- Thoroughly documented
- Properly archived
- Ready to serve as reference for future work

**Well done!**
