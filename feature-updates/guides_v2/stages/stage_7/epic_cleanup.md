# STAGE 7: Epic Cleanup Guide

**Guide Version:** 2.1
**Last Updated:** 2026-01-02
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
│ 5. ⚠️ COMMIT MESSAGE MUST USE NEW FORMAT                        │
│    - Format: "{commit_type}/KAI-{number}: {message}"           │
│    - commit_type is "feat" or "fix"                             │
│    - Message: 100 chars or less                                 │
│    - Body: List major features and changes                      │
│                                                                  │
│ 6. ⚠️ MERGE BRANCH TO MAIN AFTER COMMIT                         │
│    - Switch to main, pull latest                                │
│    - Merge epic branch: git merge {work_type}/KAI-{number}     │
│    - Push to origin: git push origin main                       │
│                                                                  │
│ 7. ⚠️ UPDATE EPIC_TRACKER.md AFTER MERGE                        │
│    - Move epic from Active to Completed table                   │
│    - Add epic detail section with commits                       │
│    - Increment "Next Available Number"                          │
│    - Commit and push EPIC_TRACKER.md update                     │
│                                                                  │
│ 8. ⚠️ MOVE ENTIRE EPIC FOLDER (NOT INDIVIDUAL FEATURES)         │
│    - Move: feature-updates/{epic}/                              │
│    - To: feature-updates/done/{epic}/                           │
│    - Keep original epic request (.txt) in root for reference    │
│                                                                  │
│ 9. ⚠️ UPDATE CLAUDE.md IF GUIDES IMPROVED                        │
│    - Check epic_lessons_learned.md for guide improvements       │
│    - Update guides_v2/ files if needed                          │
│    - Update CLAUDE.md if workflow changed                       │
│                                                                  │
│ 10. ⚠️ VERIFY EPIC IS TRULY COMPLETE                            │
│     - All features implemented                                  │
│     - All tests passing                                         │
│     - All QC passed                                             │
│     - User testing passed                                       │
│     - No pending work                                           │
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
│   ├─ Find ALL lessons_learned.md files (systematic search)
│   ├─ Read and extract lessons from EACH file
│   ├─ Create master checklist of ALL proposed guide updates
│   ├─ Apply EACH lesson to guides (100% application required)
│   ├─ Update CLAUDE.md if workflow changed
│   └─ Verify ALL lessons applied
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
│   ├─ Merge branch to main
│   ├─ Push to origin
│   └─ Update EPIC_TRACKER.md
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
    ├─ Update EPIC_README.md with completion summary
    └─ Celebrate epic completion! 🎉
```

**Critical Decision Points:**
- **After Step 2:** If tests fail → Fix issues, RESTART Step 2
- **After Step 3:** If documentation incomplete → Update docs, re-verify
- **After Step 5:** If user finds bugs → Create bug fixes, RESTART Stage 6, return to Step 5
- **After Step 6:** If commit fails → Fix issues, retry commit

---

## Quick Navigation

**Stage 7 has 8 main steps. Jump to any step:**

| Step | Focus Area | Mandatory Gate? | Go To |
|------|-----------|-----------------|-------|
| **Step 1** | Pre-Cleanup Verification | No | [Step 1](#step-1-pre-cleanup-verification) |
| **Step 2** | Run Unit Tests | ✅ YES (100% pass) | [Step 2](#step-2-run-unit-tests) |
| **Step 2b** | Investigate Anomalies | Optional | [Step 2b](#step-2b-investigate-user-reported-anomalies-if-applicable) |
| **Step 3** | Documentation Verification | No | [Step 3](#step-3-documentation-verification) |
| **Step 4** | Update Guides (Apply Lessons) | No | [Step 4](#step-4-update-guides-if-needed) |
| **Step 5** | User Testing & Bug Fix Protocol | ✅ YES (ZERO bugs) | [Step 5](#step-5-user-testing--bug-fix-protocol) |
| **Step 6** | Final Commit | No | [Step 6](#step-6-final-commit) |
| **Step 7** | Move Epic to done/ | No | [Step 7](#step-7-move-epic-to-done-folder) |
| **Step 8** | Final Verification & Completion | No | [Step 8](#step-8-final-verification--completion) |

**Reference Files (Extracted for Quick Access):**

| Reference | Description | Location |
|-----------|-------------|----------|
| **Commit Message Examples** | Format, examples, anti-patterns | [STAGE_7_reference/commit_message_examples.md](STAGE_7_reference/commit_message_examples.md) |
| **Epic Completion Template** | EPIC_README completion format | [STAGE_7_reference/epic_completion_template.md](STAGE_7_reference/epic_completion_template.md) |
| **Lessons Learned Guide** | How to extract and apply lessons | [STAGE_7_reference/lessons_learned_examples.md](STAGE_7_reference/lessons_learned_examples.md) |

**Key Sections:**

| Section | Description | Go To |
|---------|-------------|-------|
| Critical Rules | Must-follow cleanup rules | [Critical Rules](#critical-rules) |
| Prerequisites | What must be done first | [Prerequisites Checklist](#prerequisites-checklist) |
| Completion Criteria | All items that must be checked | [Completion Criteria](#completion-criteria) |

**Important:**
- Step 2: 100% test pass required (MANDATORY)
- Step 4: Apply ALL lessons from ALL sources (epic + features + bugfixes)
- Step 5: User testing with ZERO bugs required (MANDATORY)

---

## Detailed Workflow

### STEP 1: Pre-Cleanup Verification

**Objective:** Verify epic is truly complete and ready for cleanup.

**Actions:**

**1a. Verify Stage 6 Complete**

Read EPIC_README.md "Epic Progress Tracker" section and verify Stage 6 shows ✅ COMPLETE with all sub-items checked.

**If Stage 6 NOT complete:** STOP Stage 7, return to Stage 6, complete Stage 6 fully.

**1b. Verify All Features Complete**

Check EPIC_README.md "Epic Progress Tracker" to verify ALL features show ✅ through Stage 5e.

**1c. Verify No Pending Work**

Check epic folder for any incomplete work:
```bash
ls feature-updates/{epic_name}/
```

Look for:
- ❌ Any feature folders without "Stage 5e complete" in README.md
- ❌ Any bugfix folders without "Stage 5c complete" in README.md
- ❌ Any folders with "IN PROGRESS" status
- ❌ Any temporary files (*.tmp, *.bak, etc.)

**If pending work found:** STOP Stage 7, complete pending work, return when all work complete.

**1d. Read epic_lessons_learned.md**

Use Read tool to load epic_lessons_learned.md and look for "Guide Improvements Needed" sections. Document guide improvements needed for Step 4.

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

**Note:** It is ACCEPTABLE to fix pre-existing test failures during Stage 7 to achieve 100% pass rate.

---

### STEP 2b: Investigate User-Reported Anomalies (If Applicable)

**Objective:** Verify root cause of unexpected behavior empirically.

**When to use:** User notices unexpected behavior during testing (e.g., "all players have same value")

**⚠️ CRITICAL RULE:** Do NOT assume existing code comments/warnings explain the behavior - verify empirically.

**Actions:**

1. **Create test script to verify behavior directly** against source of truth
2. **Compare expected vs actual behavior** (test current scenario vs control)
3. **Update documentation** if root cause differs from assumptions
4. **Document investigation** in epic_lessons_learned.md

**See:** `STAGE_7_ORIGINAL_BACKUP.md` lines 398-505 for detailed investigation protocol.

---

### STEP 3: Documentation Verification

**Objective:** Verify all epic documentation is complete and accurate.

**Actions:**

**3a. Verify EPIC_README.md Complete**

Read EPIC_README.md and verify all sections present:
- 🎯 Quick Reference Card
- Agent Status
- Epic Overview
- Epic Progress Tracker
- Feature Summary
- Epic-Level Files
- Workflow Checklist

Verify:
- ✅ All sections present
- ✅ Information accurate and up-to-date
- ✅ No placeholder text (e.g., "TODO", "{fill in later}")
- ✅ Dates are correct
- ✅ Feature list matches actual features

**If incomplete:** Update missing sections, fix inaccurate information, remove placeholder text.

**3b. Verify epic_lessons_learned.md Contains Insights**

Read epic_lessons_learned.md and verify:
- ✅ Insights from ALL stages present (Stages 1-6)
- ✅ Lessons from ALL features documented
- ✅ "Guide Improvements Needed" sections present
- ✅ Cross-epic insights documented
- ✅ Recommendations actionable

**If incomplete:** Add missing stage insights, document lessons from all features, add cross-epic patterns.

**3c. Verify epic_smoke_test_plan.md Accurate**

Read epic_smoke_test_plan.md and verify:
- ✅ "Last Updated" shows recent Stage 5e update
- ✅ Update History table shows all features contributed
- ✅ Test scenarios reflect ACTUAL implementation
- ✅ Integration tests included (added during Stage 5e)
- ✅ Epic success criteria still accurate

**If outdated:** Update test plan to reflect final implementation.

**3d. Verify All Feature README.md Files Complete**

For EACH feature folder, read README.md and verify:
- ✅ README.md exists
- ✅ All sections present
- ✅ Status shows "Stage 5e complete"
- ✅ No placeholders or TODOs
- ✅ Workflow checklist all checked

**If ANY feature README incomplete:** Update incomplete README files.

---

### STEP 4: Update Guides (If Needed)

**Objective:** Apply ALL lessons learned from ALL sources to improve guides for future epics.

**⚠️ CRITICAL:** Do NOT only check epic_lessons_learned.md. You MUST check ALL lesson sources.

**Actions:**

**4a. Find ALL Lessons Learned Files (SYSTEMATIC SEARCH)**

Use bash to find ALL lessons learned files in the epic:
```bash
find feature-updates/done/{epic_name} -name "lessons_learned.md" -type f
```

**Expected Results:**
```
feature-updates/done/{epic_name}/epic_lessons_learned.md
feature-updates/done/{epic_name}/feature_01_{name}/lessons_learned.md
feature-updates/done/{epic_name}/feature_02_{name}/lessons_learned.md
feature-updates/done/{epic_name}/bugfix_{priority}_{name}/lessons_learned.md
...
```

**⚠️ MANDATORY:** You MUST check ALL files found, not just some.

**4b. Read and Extract Lessons from EACH File**

For EACH lessons_learned.md file found, read it completely and extract "Guide Improvements Needed" sections.

**Reference:** See `STAGE_7_reference/lessons_learned_examples.md` for examples of lesson structures and extraction methods.

**4c. Create Master Checklist of ALL Proposed Guide Updates**

Combine ALL lessons from ALL files into one comprehensive checklist.

**4d. Apply EACH Lesson to Guides**

For EACH lesson in master checklist:
1. Read current guide using Read tool
2. Locate section needing improvement
3. Add example, clarification, or new step
4. Use Edit tool to update guide
5. Mark lesson as [x] APPLIED in master checklist

**4e. Verify ALL Lessons Applied**

**Before proceeding, verify:**
```markdown
## Verification: All Lessons Applied

□ Read ALL lessons_learned.md files (epic + features + bugfixes)
□ Created master checklist with {N} total lessons
□ Applied ALL {N} lessons to guides (none skipped)
□ Each lesson marked [x] APPLIED in checklist
□ Can cite which guide section was updated for each lesson

**Master Checklist Status:**
- Total lessons identified: {N}
- Lessons applied: {N}
- Lessons skipped: 0 ✅
- Application rate: 100% ✅
```

**If application rate < 100%:** ❌ STOP - Apply remaining lessons.

**4f. Update CLAUDE.md (If Workflow Changed)**

If epic revealed workflow improvements (new stages, stage dependencies changed, critical rules updated), update CLAUDE.md accordingly.

**Reference:** See `STAGE_7_ORIGINAL_BACKUP.md` lines 858-933 for detailed guide update documentation template.

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

**Please test the system and report:**
- "No bugs found" - if everything works correctly
- OR: List of bugs/issues discovered (one per line with description)

I'll wait for your testing results before proceeding with the final commit.
```

**5b. Wait for User Testing Results**

**DO NOT PROCEED** until user responds with testing results.

**Possible outcomes:**
- **Outcome 1:** User reports "No bugs found" → ✅ Proceed to Step 6 (Final Commit)
- **Outcome 2:** User reports bugs/issues → ⚠️ STOP Stage 7, follow bug fix protocol (see Step 5c)

**5c. Bug Fix Protocol (If User Found Bugs)**

If user reports ANY bugs:

**Phase 1: Document Bugs**
1. Create bug fix folder: `feature-updates/{epic_name}/bugfix_{priority}_{name}/`
2. Determine priority (high/medium/low)
3. Create notes.txt in bug fix folder
4. User verifies notes.txt (ask user to confirm bug description is accurate)

**Phase 2: Fix ALL Bugs**
1. Read bug fix workflow guide: `stages/stage_5/bugfix_workflow.md`
2. Follow bug fix stages: Stage 2 → 5a → 5b → 5c
3. Mark bug fix complete in EPIC_README.md
4. Repeat for all bugs until ALL bug fixes reach Stage 5c

**Phase 3: RESTART Stage 6 (Epic Final QC)**

⚠️ **CRITICAL:** After ALL bugs are fixed, you MUST restart the entire Stage 6 process:
1. Read Stage 6 guide again
2. Execute epic smoke testing (4 parts)
3. Execute epic QC rounds (3 rounds)
4. Execute epic PR review (11 categories)
5. Validate against original epic request

**If Stage 6 finds MORE bugs:** Create new bug fixes, RESTART Stage 6 AGAIN, repeat until Stage 6 passes with ZERO issues.

**Phase 4: Return to Step 5 (User Testing Again)**
1. Return to Step 5a (User Testing)
2. Ask user to test again to verify bugs are fixed
3. If user finds MORE bugs: Repeat Phase 1-4
4. If user reports "No bugs found": Proceed to Step 6 (Final Commit)

**5d. Document User Testing Completion**

Once user testing passes with ZERO bugs, update EPIC_README.md with user testing results.

**Why User Testing is Critical:**
- Agent testing has blind spots - agents focus on technical correctness, may miss usability issues
- User perspective is unique - users test realistic workflows agents might not consider
- Real-world validation - user testing with real data catches issues automated tests miss
- Final quality gate - ensures epic truly works before committing to codebase

**User Testing is MANDATORY** - do NOT skip this step.

**Reference:** See `STAGE_7_ORIGINAL_BACKUP.md` lines 936-1153 for detailed bug fix protocol and user testing documentation.

---

### STEP 6: Final Commit

**Objective:** Commit all epic changes to git with clear, descriptive message.

**Actions:**

**6a. Review All Changes**

Check git status and diff:
```bash
git status
git diff {modified_files}
```

Verify:
- ✅ All changes related to epic
- ✅ No unrelated changes included
- ✅ No debugging code left in (e.g., print statements)
- ✅ No commented-out code
- ✅ No sensitive data (API keys, passwords, etc.)

**6b. Stage All Epic Changes**

Add all epic-related changes:
```bash
# Stage modified files
git add {file1} {file2} {file3}

# Stage epic folder (all files)
git add feature-updates/{epic_name}/
```

**6c. Create Commit with Clear Message**

**Commit Message Format:**
```
{commit_type}/KAI-{number}: Complete {epic_name} epic

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

**Where:**
- `{commit_type}` = `feat` (feature epic) or `fix` (bug fix epic)
- `{number}` = KAI number from EPIC_TRACKER.md and branch name
- Message limit: 100 chars or less for first line

**Reference:** See `STAGE_7_reference/commit_message_examples.md` for detailed examples and anti-patterns.

**Create commit using HEREDOC:**
```bash
git commit -m "$(cat <<'EOF'
feat/KAI-1: Complete improve_draft_helper epic

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

Verify commit message clear, all epic files included, file change counts reasonable.

**6e. Merge Branch to Main**

**CRITICAL:** Merge the epic branch to main after commit is complete.

Switch to main branch:
```bash
git checkout main
```

Pull latest changes from origin:
```bash
git pull origin main
```

Merge epic branch into main:
```bash
git merge {work_type}/KAI-{number}
```

**Example:**
```bash
git merge epic/KAI-1
```

**If merge conflicts occur:** Review conflicts carefully, resolve conflicts, stage resolved files, complete merge.

Verify merge successful:
```bash
git log -1
```

**6f. Push to Remote**

Push merged changes to origin main:
```bash
git push origin main
```

Verify push successful:
```bash
git status
```

**Expected:** "Your branch is up to date with 'origin/main'", "nothing to commit, working tree clean"

**6g. Update EPIC_TRACKER.md**

1. **Move epic from Active to Completed table**
2. **Increment "Next Available Number"**
3. **Add Epic Detail Section** with:
   - Epic description
   - Features implemented
   - Key changes
   - Commit history (use `git log --oneline --grep="KAI-{number}"`)
   - Testing results
   - Link to lessons learned

**Commit EPIC_TRACKER.md update:**
```bash
git add feature-updates/EPIC_TRACKER.md
git commit -m "feat/KAI-1: Update EPIC_TRACKER with completed epic details"
git push origin main
```

**6h. Delete Epic Branch (Optional)**

```bash
git branch -d {work_type}/KAI-{number}
```

**Example:**
```bash
git branch -d epic/KAI-1
```

---

### STEP 7: Move Epic to done/ Folder

**Objective:** Move completed epic folder to done/ for archival.

**Actions:**

**7a. Create done/ Folder (If Doesn't Exist)**

Check if done/ folder exists:
```bash
ls feature-updates/
```

If done/ doesn't exist:
```bash
mkdir feature-updates/done
```

**7b. Move Entire Epic Folder to done/**

Move the complete epic folder:

**Windows:**
```bash
move feature-updates\{epic_name} feature-updates\done\{epic_name}
```

**Linux/Mac:**
```bash
mv feature-updates/{epic_name} feature-updates/done/{epic_name}
```

**CRITICAL:** Move the ENTIRE folder, not individual features.

**7c. Verify Move Successful**

Check folder structure:
```bash
ls feature-updates/done/{epic_name}/
```

**Expected:**
```
EPIC_README.md
epic_smoke_test_plan.md
epic_lessons_learned.md
feature_01_{name}/
feature_02_{name}/
feature_03_{name}/
bugfix_{priority}_{name}/  (if bug fixes existed)
```

Verify:
- ✅ All features present
- ✅ All epic-level files present
- ✅ All bug fix folders present (if any)
- ✅ No files left behind in original location

**7d. Leave Original Epic Request in Root**

**IMPORTANT:** Do NOT move the original {epic_name}.txt file.

**Why:** Original request stays in feature-updates/ root for reference.

Verify:
```bash
ls feature-updates/{epic_name}.txt
```

**Expected:** File still exists in root.

---

### STEP 8: Final Verification & Completion

**Objective:** Verify epic cleanup complete and celebrate completion!

**Actions:**

**8a. Verify Epic in done/ Folder**

Confirm epic moved successfully:
```bash
ls feature-updates/done/
```

**8b. Verify Original Request Still in Root**

Confirm original request accessible:
```bash
ls feature-updates/{epic_name}.txt
```

**8c. Verify Git Shows Clean State**

Check git status:
```bash
git status
```

**Expected:** "Your branch is up to date with 'origin/main'", "nothing to commit, working tree clean" (or folder rename not staged - this is optional)

**8d. Update EPIC_README.md One Final Time**

Update the EPIC_README.md in done/ folder with epic completion summary.

**Reference:** See `STAGE_7_reference/epic_completion_template.md` for detailed template and instructions.

**Template:**
```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** Stage 7 - Epic Cleanup
**Status:** ✅ COMPLETE

**Epic Completion Summary:**
- Start Date: {YYYY-MM-DD}
- End Date: {YYYY-MM-DD}
- Duration: {N} days
- Total Features: {N}
- Bug Fixes Created: {N}
- Final Test Pass Rate: 100% ({total_tests}/{total_tests} tests)

**Epic Moved To:** feature-updates/done/{epic_name}/
**Original Request:** feature-updates/{epic_name}.txt

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

---

## Re-Reading Checkpoints

**You MUST re-read this guide when:**

1. **After Session Compaction** - Check EPIC_README.md Agent Status to see which step you're on
2. **After Test Failures** - Re-read after fixing tests
3. **After Commit Failures** - Re-read commit requirements
4. **Before Moving Epic** - Re-read move instructions
5. **When Encountering Confusion** - Re-read workflow overview and current step

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
- [ ] Found ALL lessons_learned.md files (systematic search)
- [ ] Read ALL files (epic + features + bugfixes)
- [ ] Created master checklist of ALL lessons
- [ ] Applied ALL lessons to guides (100% application rate)
- [ ] Updated CLAUDE.md if workflow changed

### User Testing
- [ ] User tested complete system
- [ ] User testing result: ZERO bugs found
- [ ] If bugs found: All fixed, Stage 6 re-run, user re-tested

### Git Commit
- [ ] All changes reviewed with git status and git diff
- [ ] All epic changes staged
- [ ] Commit created with clear, descriptive message
- [ ] Commit successful (verified with git log)
- [ ] Branch merged to main
- [ ] Pushed to remote
- [ ] EPIC_TRACKER.md updated

### Epic Move
- [ ] done/ folder exists
- [ ] Entire epic folder moved to done/
- [ ] Epic folder structure intact in done/
- [ ] Original epic request (.txt) still in root

### Final Verification
- [ ] Epic visible in done/ folder
- [ ] Original request accessible in root
- [ ] Git status clean
- [ ] EPIC_README.md updated with completion status

**Epic is COMPLETE when ALL completion criteria are met.**

---

## Summary

**Stage 7 - Epic Cleanup finalizes the epic and archives it for future reference:**

**Key Activities:**
1. Run unit tests (100% pass required)
2. Verify all documentation complete
3. Apply ALL lessons learned to guides (systematic search, 100% application)
4. User testing (MANDATORY - cannot skip)
5. Commit all changes to git with clear message
6. Merge branch to main, update EPIC_TRACKER.md
7. Move entire epic folder to done/
8. Leave original epic request in root for reference
9. Celebrate epic completion! 🎉

**Critical Success Factors:**
- 100% test pass rate before committing
- Complete documentation (README, lessons learned, test plan)
- ALL lessons applied (not just epic lessons - features + bugfixes too)
- User testing passed with ZERO bugs
- Clear, descriptive commit message
- Entire epic folder moved (not individual features)

**Common Pitfalls:**
- Committing without running tests
- Generic commit messages
- Only checking epic_lessons_learned.md (missing feature/bugfix lessons)
- Skipping user testing
- Moving features individually instead of entire epic
- Moving original request file (should stay in root)

**Reference Files:**
- `STAGE_7_reference/commit_message_examples.md` - Commit message format and examples
- `STAGE_7_reference/epic_completion_template.md` - EPIC_README.md completion template
- `STAGE_7_reference/lessons_learned_examples.md` - Lesson extraction and application guide
- `STAGE_7_ORIGINAL_BACKUP.md` - Original guide with all inline examples

---

**END OF STAGE 7 GUIDE**

---

**🎉 CONGRATULATIONS! 🎉**

If you've completed Stage 7, you've successfully finished an entire epic from start to finish. The epic is now production-ready, fully tested (100% pass rate), thoroughly documented, and properly archived.

**Well done!**
