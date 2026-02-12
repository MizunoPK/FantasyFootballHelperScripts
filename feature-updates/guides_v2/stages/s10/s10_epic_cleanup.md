# S10: Epic Cleanup Guide

**Guide Version:** 2.1
**Last Updated:** 2026-01-02
**Prerequisites:** S9 complete (Epic Final QC passed)
**Next Stage:** None (Epic complete - moved to done/)

---

## Table of Contents

1. [MANDATORY READING PROTOCOL](#mandatory-reading-protocol)
2. [Overview](#overview)
3. [Critical Rules](#critical-rules)
4. [Prerequisites Checklist](#prerequisites-checklist)
5. [Workflow Overview](#workflow-overview)
6. [Quick Navigation](#quick-navigation)
7. [Detailed Workflow](#detailed-workflow)
8. [Re-Reading Checkpoints](#re-reading-checkpoints)
9. [Exit Criteria](#exit-criteria)
10. [Summary](#summary)

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting S10, you MUST:**

1. **Read this ENTIRE guide** using the Read tool
2. **Use the phase transition prompt** from `prompts_reference_v2.md` ("Starting Epic Cleanup")
3. **Acknowledge critical requirements** by listing them explicitly
4. **Verify ALL prerequisites** using the checklist below
5. **Update EPIC_README.md Agent Status** to reflect S10 start
6. **THEN AND ONLY THEN** begin epic cleanup

**Rationale:** S10 is the FINAL stage before epic completion. This stage ensures:
- All work is committed to git
- Documentation is complete and accurate
- Epic folder is ready for archival
- Future agents can understand what was accomplished

Rushing this process results in incomplete documentation, missing commits, or disorganized done/ folder.

---

## Overview

**What is S10?**
Epic Cleanup is the final stage where you commit all changes, verify documentation, and move the completed epic to the done/ folder for archival.

**When do you use this guide?**
- After S9 (Epic Final QC) is complete
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

```text
┌─────────────────────────────────────────────────────────────────┐
│ CRITICAL RULES FOR STAGE 10                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 1. ⚠️ STAGE 6 MUST BE COMPLETE                                  │
│    - Verify Epic Final QC passed                                │
│    - Verify no pending bug fixes or features                    │
│    - Verify EPIC_README.md shows S9 complete               │
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
│ 4. ⚠️ USER TESTING COMPLETED IN STAGE 6                         │
│    - S9 includes mandatory user testing (Step 6)           │
│    - User must report "No bugs found" before S10            │
│    - If bugs found in S9 → Bug fixes → Restart S6    │
│    - S10 only begins after user testing passed              │
│                                                                  │
│ 5. ⚠️ COMMIT MESSAGE MUST USE NEW FORMAT                        │
│    - Format: "{commit_type}/KAI-{number}: {message}"           │
│    - commit_type is "feat" or "fix"                             │
│    - Message: 100 chars or less                                 │
│    - Body: List major features and changes                      │
│                                                                  │
│ 6. ⚠️ CREATE PULL REQUEST FOR USER REVIEW                       │
│    - Push branch to remote: git push origin {work_type}/KAI-{N}│
│    - Create PR using gh CLI with epic summary                   │
│    - User reviews PR and merges when satisfied                  │
│                                                                  │
│ 7. ⚠️ UPDATE EPIC_TRACKER.md BEFORE CREATING PR                │
│    - Move epic from Active to Completed table                   │
│    - Add epic detail section with commits                       │
│    - Increment "Next Available Number"                          │
│    - Commit and push EPIC_TRACKER.md update as part of PR       │
│                                                                  │
│ 8. ⚠️ MOVE ENTIRE EPIC FOLDER (NOT INDIVIDUAL FEATURES)         │
│    - Move: feature-updates/{epic}/                              │
│    - To: feature-updates/done/{epic}/                           │
│    - Keep original epic request (.txt) in root for reference    │
│                                                                  │
│ 9. ⚠️ MAINTAIN MAX 10 EPICS IN done/ FOLDER                     │
│    - Count epics in done/ before moving current epic            │
│    - If count >= 10: Delete oldest epic(s) to make room         │
│    - After move: done/ should have 10 or fewer epics            │
│    - Keeps repository size manageable                           │
│                                                                  │
│ 10. ⚠️ UPDATE CLAUDE.md IF GUIDES IMPROVED                       │
│    - Check epic_lessons_learned.md for guide improvements       │
│    - Update guides_v2/ files if needed                          │
│    - Update CLAUDE.md if workflow changed                       │
│                                                                  │
│ 11. ⚠️ VERIFY EPIC IS TRULY COMPLETE                            │
│     - All features implemented                                  │
│     - All tests passing                                         │
│     - All QC passed                                             │
│     - User testing passed (completed in S9 Step 6)         │
│     - No pending work                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites Checklist

**Before starting S10, verify:**

### S9 Completion
- [ ] EPIC_README.md shows "S9 - Epic Final QC: ✅ COMPLETE"
- [ ] Epic smoke testing passed (S9.P1)
- [ ] Epic QC Validation Loop passed (3 consecutive clean rounds in S9.P2)
- [ ] User testing passed (Step 6 - ZERO bugs reported by user)
- [ ] Epic PR review passed (all 11 categories)
- [ ] No pending issues from S9

### Feature Completion Status
- [ ] ALL features show "S8.P2 (Epic Testing Update) complete" in EPIC_README.md
- [ ] No features in progress
- [ ] No pending bug fixes (or all bug fixes at S7 (Testing & Review))

### Test Status
- [ ] All unit tests passing (verified recently)
- [ ] No test failures
- [ ] No skipped tests

### Documentation Status
- [ ] EPIC_README.md exists and is complete
- [ ] epic_lessons_learned.md exists with insights from all stages
- [ ] epic_smoke_test_plan.md reflects final implementation
- [ ] All feature README.md files complete

**If ANY checklist item is unchecked, STOP. Do NOT proceed to S10 until all prerequisites are met.**

---

## Workflow Overview

```text
STAGE 10: Epic Cleanup
│
├─> STEP 1: Pre-Cleanup Verification (Verify epic truly complete)
│   ├─ Verify S9 complete
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
├─> STEP 5: Final Commit (Epic Implementation)
│   ├─ Review all changes with git status and git diff
│   ├─ Stage all epic-related changes
│   ├─ Create commit with clear message
│   └─ Verify commit successful
│
├─> STEP 6: Move Epic to done/ Folder
│   ├─ Create done/ folder if doesn't exist
│   ├─ Clean up done/ folder (max 10 epics, delete oldest if needed)
│   ├─ Move entire epic folder to done/
│   ├─ Verify move successful (folder structure intact)
│   ├─ Verify done/ has 10 or fewer epics
│   ├─ Leave original epic request (.txt) in root for reference
│   └─ Commit the epic folder move
│
├─> STEP 7: Update EPIC_TRACKER.md
│   ├─ Move epic from Active to Completed table
│   ├─ Add epic detail section with full description
│   ├─ Increment "Next Available Number"
│   └─ Commit the EPIC_TRACKER.md update
│
├─> STEP 8: Push Branch and Create Pull Request
│   ├─ Push all commits to remote branch
│   ├─ Create Pull Request for user review
│   └─ Wait for user to merge PR
│
└─> STEP 9: Final Verification & Completion
    ├─ Verify epic in done/ folder
    ├─ Verify original request still in root
    ├─ Verify git shows clean state
    ├─ Update EPIC_README.md with completion summary
    └─ Celebrate epic completion! 🎉
```

**Critical Decision Points:**
- **After Step 2:** If tests fail → Fix issues, RESTART Step 2
- **After Step 3:** If documentation incomplete → Update docs, re-verify
- **After Step 5:** If commit fails → Fix issues, retry commit

---

## Quick Navigation

**S10 has 9 main steps. Jump to any step:**

| Step | Focus Area | Time | Mandatory Gate? | Go To |
|------|-----------|------|-----------------|-------|
| **Step 1** | Pre-Cleanup Verification | 5 min | No | [Jump](#step-1-pre-cleanup-verification) |
| **Step 2** | Run Unit Tests | 5 min | ✅ YES (100% pass) | [Jump](#step-2-run-unit-tests) |
| **Step 2b** | Investigate Anomalies | 10-30 min | Optional | [Jump](#step-2b-investigate-user-reported-anomalies-if-applicable) |
| **Step 3** | Documentation Verification | 10 min | No | [Jump](#step-3-documentation-verification) |
| **Step 4** | Update Guides (Apply Lessons) | 20-45 min | No | [Jump](#step-4-update-guides-if-needed) |
| **Step 5** | Final Commit (Epic Work) | 10 min | No | [Jump](#step-5-final-commit-epic-implementation) |
| **Step 6** | Move Epic to done/ | 5 min | No | [Jump](#step-6-move-epic-to-done-folder) |
| **Step 7** | Update EPIC_TRACKER.md | 5 min | No | [Jump](#step-7-update-epic_trackermd) |
| **Step 8** | Push and Create PR | 5 min | No | [Jump](#step-8-push-branch-and-create-pull-request) |
| **Step 9** | Final Verification | 5 min | No | [Jump](#step-9-final-verification--completion) |

**Total Time:** 85-130 minutes (including S10.P1 guide updates)

**Reference Files (Extracted for Quick Access):**

| Reference | Description | Location |
|-----------|-------------|----------|
| **Commit Message Examples** | Format, examples, anti-patterns | [reference/stage_10/commit_message_examples.md](../../reference/stage_10/commit_message_examples.md) |
| **Epic Completion Template** | EPIC_README completion format | [reference/stage_10/epic_completion_template.md](../../reference/stage_10/epic_completion_template.md) |
| **Lessons Learned Guide** | How to extract and apply lessons | [reference/stage_10/lessons_learned_examples.md](../../reference/stage_10/lessons_learned_examples.md) |

**Key Sections:**

| Section | Description | Go To |
|---------|-------------|-------|
| Critical Rules | Must-follow cleanup rules | [Critical Rules](#critical-rules) |
| Prerequisites | What must be done first | [Prerequisites Checklist](#prerequisites-checklist) |
| Completion Criteria | All items that must be checked | [Completion Criteria](#completion-criteria) |

**Important:**
- Step 2: 100% test pass required (MANDATORY)
- Step 4: Apply ALL lessons from ALL sources (epic + features + bugfixes + debugging)
- User testing completed in S9 Step 6 (prerequisite for S10)

---

## Detailed Workflow

### STEP 1: Pre-Cleanup Verification

**Objective:** Verify epic is truly complete and ready for cleanup.

**Actions:**

**1a. Verify S9 Complete**

Read EPIC_README.md "Epic Progress Tracker" section and verify S9 shows ✅ COMPLETE with all sub-items checked.

**If S9 NOT complete:** STOP S10, return to S9, complete S9 fully.

**1b. Verify All Features Complete**

Check EPIC_README.md "Epic Progress Tracker" to verify ALL features show ✅ through S8.P2 (Epic Testing Update).

**1c. Verify No Pending Work**

Check epic folder for any incomplete work:
```bash
ls feature-updates/{epic_name}/
```

Look for:
- ❌ Any feature folders without "S8.P2 (Epic Testing Update) complete" in README.md
- ❌ Any bugfix folders without "S7 (Testing & Review) complete" in README.md
- ❌ Any folders with "IN PROGRESS" status
- ❌ Any temporary files (*.tmp, *.bak, etc.)

**If pending work found:** STOP S10, complete pending work, return when all work complete.

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
```bash
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

**Note:** It is ACCEPTABLE to fix pre-existing test failures during S10 to achieve 100% pass rate.

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
- ✅ "Last Updated" shows recent S8.P2 (Epic Testing Update) update
- ✅ Update History table shows all features contributed
- ✅ Test scenarios reflect ACTUAL implementation
- ✅ Integration tests included (added during S8.P2 (Epic Testing Update))
- ✅ Epic success criteria still accurate

**If outdated:** Update test plan to reflect final implementation.

**3d. Verify All Feature README.md Files Complete**

For EACH feature folder, read README.md and verify:
- ✅ README.md exists
- ✅ All sections present
- ✅ Status shows "S8.P2 (Epic Testing Update) complete"
- ✅ No placeholders or TODOs
- ✅ Workflow checklist all checked

**If ANY feature README incomplete:** Update incomplete README files.

---

### STEP 4: Guide Update from Lessons Learned (🚨 MANDATORY - S10.P1)

**Objective:** Apply lessons learned from epic to improve guides for future agents using systematic user-approved workflow.

**⚠️ CRITICAL:** This is NOT optional. Every epic must run S10.P1 to continuously improve guides.

**READ THE FULL GUIDE:**
```text
stages/s10/s10_p1_guide_update_workflow.md
```

**Process Overview:**
1. Analyze all lessons_learned.md files (epic + all features)
2. Create GUIDE_UPDATE_PROPOSAL.md with prioritized proposals (P0-P3)
3. Present each proposal to user for individual approval
4. Apply only approved changes to guides
5. Create separate commit for guide updates
6. Update guide_update_tracking.md

**Time Estimate:** 20-45 minutes

**Exit Condition:** S10.P1 complete (verify guide_update_tracking.md updated if changes applied)

**NEXT:** After S10.P1 complete, proceed to STEP 5 (Final Commit) for epic code

---

### STEP 5: Final Commit (Epic Implementation)

**Objective:** Commit all epic implementation work (code changes, tests, documentation) with clear, descriptive message. This is the main epic commit - epic folder move and EPIC_TRACKER.md update will be separate commits in Steps 6-7.

**Actions:**

**5a. Review All Changes**

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

**5b. Stage All Epic Changes**

Add all epic-related changes:
```bash
## Stage modified files
git add {file1} {file2} {file3}

## Stage epic folder (all files)
git add feature-updates/{epic_name}/
```text

**5c. Create Commit with Clear Message**

**Commit Message Format:**
```text
{commit_type}/KAI-{number}: Complete {epic_name} epic

Major features:
- {Feature 1 brief description}
- {Feature 2 brief description}

Key changes:
- {File 1}: {What changed and why}
- {File 2}: {What changed and why}

Testing:
- All unit tests passing (2200/2200)
- Epic smoke testing passed
- Epic QC Validation Loop passed (3 consecutive clean rounds)
```

**Where:**
- `{commit_type}` = `feat` (feature epic) or `fix` (bug fix epic)
- `{number}` = KAI number from EPIC_TRACKER.md and branch name
- Message limit: 100 chars or less for first line

**Detailed Examples:** See `reference/stage_10/commit_message_examples.md` for complete examples, anti-patterns, and variations.

**Create commit using HEREDOC** (ensures proper formatting):
```bash
git commit -m "$(cat <<'EOF'
feat/KAI-{N}: Complete {epic_name} epic

{content following format above}
EOF
)"
```

**5d. Verify Commit Successful**

Check git log:
```bash
git log -1 --stat
```

Verify commit message clear, all epic files included, file change counts reasonable.

**Note:** Do NOT push yet - Steps 6-7 will create additional commits (epic folder move, EPIC_TRACKER.md update) that should all be part of the same PR.

---

### STEP 6: Move Epic to done/ Folder

**Objective:** Move completed epic folder to done/ for archival.

**Actions:**

**6a. Create done/ Folder (If Doesn't Exist)**

Check if done/ folder exists:
```bash
ls feature-updates/
```

If done/ doesn't exist:
```bash
mkdir feature-updates/done
```

**6b. Clean Up done/ Folder (Max 10 Epics)**

**Purpose:** Maintain a maximum of 10 archived epics in done/ folder by deleting oldest epics when needed.

**Check current epic count:**
```bash
## Count directories in done/ (excluding guides_v2)
ls -d feature-updates/done/*/ | wc -l
```

**If count is 10 or more:**

1. **List epics by date (oldest first):**
   ```bash
   # Windows (PowerShell)
   Get-ChildItem feature-updates\done -Directory | Sort-Object LastWriteTime | Select-Object Name, LastWriteTime

   # Linux/Mac
   ls -lt feature-updates/done/ | tail -n +2
   ```

2. **Calculate how many to delete:**
   - Current count: {N}
   - Will add: 1 (current epic)
   - Total: {N+1}
   - Need to delete: {N+1-10} oldest epics

3. **Delete oldest epic(s):**
   ```bash
   # Windows
   rmdir /s /q feature-updates\done\{oldest_epic_name}

   # Linux/Mac
   rm -rf feature-updates/done/{oldest_epic_name}
   ```

4. **Repeat for each epic that needs deletion**

5. **Verify count after deletion:**
   ```bash
   ls -d feature-updates/done/*/ | wc -l
   ```

   **Expected:** 9 or fewer (leaving room for current epic)

**If count is less than 10:**
- No deletion needed
- Proceed to next step

**⚠️ IMPORTANT:**
- Always keep the 10 MOST RECENT epics
- Delete the OLDEST epics first
- After deletion, done/ should have 9 or fewer epics (before adding current)
- This keeps the repository size manageable
- Older epics are preserved in git history if needed

**6c. Move Entire Epic Folder to done/**

Move the complete epic folder (with KAI number):

**Windows:**
```bash
move feature-updates\KAI-{N}-{epic_name} feature-updates\done\KAI-{N}-{epic_name}
```

**Example:** `move feature-updates\KAI-1-improve_draft_helper feature-updates\done\KAI-1-improve_draft_helper`

**Linux/Mac:**
```bash
mv feature-updates/KAI-{N}-{epic_name} feature-updates/done/KAI-{N}-{epic_name}
```

**Example:** `mv feature-updates/KAI-1-improve_draft_helper feature-updates/done/KAI-1-improve_draft_helper`

**CRITICAL:** Move the ENTIRE folder, not individual features.

**6d. Verify Move Successful**

Check folder structure:
```bash
ls feature-updates/done/KAI-{N}-{epic_name}/
```

**Example:** `ls feature-updates/done/KAI-1-improve_draft_helper/`

**Expected:**
```text
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

**6e. Verify done/ Folder Count**

Check total epics in done/:
```bash
ls -d feature-updates/done/*/ | wc -l
```

**Expected:** 10 or fewer

**If count exceeds 10:**
- Review what was deleted in Step S9.P2
- Verify correct epics were removed
- Ensure only most recent 10 epics remain

**6f. Leave Original Epic Request in Root**

**IMPORTANT:** Do NOT move the original {epic_name}.txt file (if it exists in root).

**Why:** Original request stays in feature-updates/ root for reference.

**Note:** If the original request file was inside the epic folder (e.g., `KAI-8-logging_refactoring/logging_refactoring_notes.txt`), it will move with the epic folder to done/, which is acceptable.

**6g. Commit the Epic Folder Move**

Stage and commit the folder move:
```bash
git add feature-updates/done/{epic_name}/
git commit -m "chore/KAI-{N}: Move completed epic to done/ folder

Epic KAI-{N} ({epic_name}) is complete:
- All {N} features implemented and tested
- {X}/{X} tests passing
- Epic moved to done/ for clean PR state

No further changes needed after merge.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Verify commit successful:
```bash
git log -1 --oneline
```

---

### STEP 7: Update EPIC_TRACKER.md

**Objective:** Update EPIC_TRACKER.md to move epic from Active to Completed and add detailed epic information.

**Actions:**

**7a. Move Epic from Active to Completed Table**

Edit `feature-updates/EPIC_TRACKER.md`:

1. Remove the epic's row from the "Active Epics" table
2. Add the epic's row to the "Completed Epics" table with completion date and done/ location

**7b. Add Epic Detail Section**

Add a detailed section below "## Epic Details" with complete epic information (see Epic Detail Template in EPIC_TRACKER.md or KAI-6/KAI-8 examples for format):

Required information:
- Type, branch, dates, location
- Description (1-2 paragraphs)
- Features implemented (list)
- Key changes (bullet points)
- Commit history (hashes + messages)
- Testing results (test counts, smoke testing, QC rounds, user testing)
- Lessons learned (summary + link to epic_lessons_learned.md)
- Related documentation (links)

**7c. Increment Next Available Number**

Update "Next Available Number" field to KAI-{N+1}

**7d. Commit the EPIC_TRACKER.md Update**

Stage and commit:
```bash
git add feature-updates/EPIC_TRACKER.md
git commit -m "chore/KAI-{N}: Update EPIC_TRACKER with completed epic

Move KAI-{N} from Active to Completed:
- {brief epic summary}
- {key achievement}
- {key achievement}

Increment Next Available Number to KAI-{N+1}.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Verify commit successful:
```bash
git log -1 --oneline
```

---

### STEP 8: Push Branch and Create Pull Request

**Objective:** Push all commits to remote and create PR for user review.

**Actions:**

**8a. Push Branch to Remote**

Push all commits (epic work + folder move + EPIC_TRACKER update):
```bash
git push origin {work_type}/KAI-{number}
```

**8b. Create Pull Request**

Use GitHub CLI to create PR:
```bash
gh pr create --base main --head {work_type}/KAI-{number} \
  --title "{commit_type}/KAI-{number}: Complete {epic_name} epic" \
  --body "See EPIC_README.md for details. All tests passing, ready for review."
```

**Or use GitHub Web UI:**
- Navigate to repository on GitHub
- Click "Pull requests" → "New pull request"
- Select base: `main`, compare: `{work_type}/KAI-{number}`
- Fill in title and description
- Click "Create pull request"

**8c. Wait for User to Merge PR**

- User reviews changes in GitHub UI
- User approves and merges (or requests changes)
- **DO NOT merge yourself** - user must merge

**Important:** The PR includes ALL final cleanup (epic work, folder move, EPIC_TRACKER update). No further changes needed after merge.

**See:** `reference/stage_10/pr_creation_guide.md` for detailed PR templates (if exists)

---

### STEP 9: Final Verification & Completion

**Objective:** Verify epic cleanup complete and celebrate completion!

**Actions:**

**9a. Verify All Commits Pushed**

Check that all commits are on remote:
```bash
git log --oneline origin/{work_type}/KAI-{number}..HEAD
```

**Expected:** No output (all commits pushed)

**9b. Verify PR Created**

If using `gh` CLI:
```bash
gh pr view
```

Or check GitHub web UI to confirm PR exists.

**9c. Verify Git Working Tree Clean**

Check git status:
```bash
git status
```

**Expected:** "Your branch is up to date with 'origin/{work_type}/KAI-{number}'", "nothing to commit, working tree clean"

**9d. Celebrate Epic Completion! 🎉**

The epic is now complete and ready for user review!

**What was accomplished:**
- ✅ Epic planned with {N} features
- ✅ All features implemented and tested
- ✅ Epic-level integration validated
- ✅ All validation loops passed
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

## Exit Criteria

**S10 is COMPLETE when ALL of the following are true:**

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
- [ ] Read ALL files (epic + features + bugfixes + debugging)
- [ ] Created master checklist of ALL lessons
- [ ] Applied ALL lessons to guides (100% application rate)
- [ ] Updated CLAUDE.md if workflow changed

### S9 Completion (Including User Testing)
- [ ] User tested complete system (S9 Step 6)
- [ ] User testing result: ZERO bugs found
- [ ] If bugs found: All fixed, restart S9 from S9.P1 (smoke testing), user re-tested
- [ ] Epic PR review passed (all categories)

### Git Commits
- [ ] All epic changes reviewed with git status and git diff
- [ ] Epic implementation commit created with clear message
- [ ] Commit successful (verified with git log)

### Epic Move
- [ ] done/ folder exists
- [ ] done/ folder cleaned up (max 10 epics maintained)
- [ ] Entire epic folder moved to done/
- [ ] Epic folder structure intact in done/
- [ ] Epic folder move committed

### EPIC_TRACKER.md Update
- [ ] Epic moved from Active to Completed table in EPIC_TRACKER.md
- [ ] Epic detail section added with full description
- [ ] Next Available Number incremented
- [ ] EPIC_TRACKER.md update committed

### Pull Request
- [ ] All commits pushed to remote branch
- [ ] Pull Request created with epic summary
- [ ] PR includes all final cleanup (epic work + folder move + EPIC_TRACKER)
- [ ] User reviewed and merged PR
- [ ] No further changes needed after merge

### Final Verification
- [ ] Epic visible in done/ folder
- [ ] Original request accessible in root
- [ ] Git status clean
- [ ] EPIC_README.md updated with completion status

**Epic is COMPLETE when ALL completion criteria are met.**

---

## Summary

**S10 - Epic Cleanup finalizes the epic and archives it for future reference:**

**Key Activities:**
1. Run unit tests (100% pass required)
2. Verify all documentation complete
3. Apply ALL lessons learned to guides (systematic search, 100% application)
4. Commit epic implementation work with clear message
5. Move entire epic folder to done/ (max 10 epics, delete oldest if needed) and commit
6. Update EPIC_TRACKER.md (move to Completed, add details, increment number) and commit
7. Push all commits to remote branch
8. Create Pull Request for user review
9. User reviews and merges PR (no further changes needed after merge)
10. Celebrate epic completion! 🎉

**Critical Success Factors:**
- 100% test pass rate before committing
- Complete documentation (README, lessons learned, test plan)
- ALL lessons applied (epic + features + bugfixes + debugging)
- User testing already passed in S9.P3 (prerequisite)
- Clear, descriptive commit messages (separate commits for epic work, folder move, EPIC_TRACKER)
- Entire epic folder moved to done/ (not individual features)
- Max 10 epics in done/ folder maintained
- EPIC_TRACKER.md updated BEFORE creating PR
- PR includes all final cleanup (no post-merge changes needed)

**Common Pitfalls:**
- Committing without running tests
- Generic commit messages
- Only checking epic_lessons_learned.md (missing feature/bugfix/debugging lessons)
- Forgetting debugging lessons (highest priority guide updates)
  - **Why critical:** Debugging lessons from Phase 4b have highest P0/P1 priority
  - **Where to find:** {epic}/debugging/guide_update_recommendations.md
  - **What to look for:** Per-issue root causes (Phase 4b) + cross-pattern analysis (Phase 5)
  - **Application:** Debugging lessons should be applied FIRST (before general lessons)
- Moving features individually instead of entire epic
- Moving original request file (should stay in root)
- Exceeding 10 epics in done/ folder

**Reference Files:**
- `reference/stage_10/commit_message_examples.md` - Commit message format and examples
- `reference/stage_10/epic_completion_template.md` - EPIC_README.md completion template
- `reference/stage_10/lessons_learned_examples.md` - Lesson extraction and application guide
- `STAGE_7_ORIGINAL_BACKUP.md` - Original guide with all inline examples

---

## Next Stage

**🎉 EPIC COMPLETE - No Next Stage**

You've successfully completed all 10 stages of the epic workflow:
- ✅ S1: Epic Planning (Discovery, breakdown, Git setup)
- ✅ S2: Feature Deep Dives (spec.md, checklist.md for each feature)
- ✅ S3: Cross-Feature Alignment & Epic Strategy
- ✅ S4: Feature Testing Strategies
- ✅ S5-S8: Feature Loop (Planning → Execution → Testing → Alignment)
- ✅ S9: Epic-Level Final QC (100% test pass, user testing)
- ✅ S10: Epic Cleanup (guide updates, PR, archival)

**The epic is now:**
- Production-ready code (100% test pass rate)
- Fully documented (README, lessons learned)
- Properly archived (`feature-updates/done/`)
- Integrated into main branch (PR merged)

**Well done!**

---

*End of s10_epic_cleanup.md*
