# S10: Epic Cleanup Guide

**Guide Version:** 2.1
**Last Updated:** 2026-01-02
**Prerequisites:** S9 complete (Epic Final QC passed)
**Next Stage:** None (Epic complete - moved to done/)

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

## Quick Start

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

```
┌─────────────────────────────────────────────────────────────────┐
│ CRITICAL RULES FOR STAGE 7                                      │
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
│    - If bugs found in S9 → Bug fixes → Restart S6a    │
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
│ 7. ⚠️ UPDATE EPIC_TRACKER.md AFTER USER MERGES PR              │
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
- [ ] Epic smoke testing passed (all parts)
- [ ] Epic QC rounds passed (all 3 rounds)
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

```
STAGE 7: Epic Cleanup
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
├─> STEP 5: Final Commit and PR Creation
│   ├─ Review all changes with git status and git diff
│   ├─ Stage all epic-related changes
│   ├─ Create commit with clear message
│   ├─ Verify commit successful
│   ├─ Push branch to remote
│   ├─ Create Pull Request for user review
│   ├─ Wait for user to merge PR
│   └─ Update EPIC_TRACKER.md (after user merges)
│
├─> STEP 6: Move Epic to done/ Folder
│   ├─ Create done/ folder if doesn't exist
│   ├─ Clean up done/ folder (max 10 epics, delete oldest if needed)
│   ├─ Move entire epic folder to done/
│   ├─ Verify move successful (folder structure intact)
│   ├─ Verify done/ has 10 or fewer epics
│   └─ Leave original epic request (.txt) in root for reference
│
└─> STEP 7: Final Verification & Completion
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

**S10 has 7 main steps. Jump to any step:**

| Step | Focus Area | Time | Mandatory Gate? | Go To |
|------|-----------|------|-----------------|-------|
| **Step 1** | Pre-Cleanup Verification | 5 min | No | [Jump](#step-1-pre-cleanup-verification) |
| **Step 2** | Run Unit Tests | 5 min | ✅ YES (100% pass) | [Jump](#step-2-run-unit-tests) |
| **Step 2b** | Investigate Anomalies | 10-30 min | Optional | [Jump](#step-2b-investigate-user-reported-anomalies-if-applicable) |
| **Step 3** | Documentation Verification | 10 min | No | [Jump](#step-3-documentation-verification) |
| **Step 4** | Update Guides (Apply Lessons) | 20-45 min | No | [Jump](#step-4-update-guides-if-needed) |
| **Step 5** | Final Commit | 10 min | No | [Jump](#step-5-final-commit) |
| **Step 6** | Move Epic to done/ | 5 min | No | [Jump](#step-6-move-epic-to-done-folder) |
| **Step 7** | Final Verification & Completion | 5 min | No | [Jump](#step-7-final-verification--completion) |

**Total Time:** 70-115 minutes (including S10.5 guide updates)

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

### STEP 4: Guide Update from Lessons Learned (🚨 MANDATORY - S10.5)

**Objective:** Apply lessons learned from epic to improve guides for future agents using systematic user-approved workflow.

**🆕 NEW WORKFLOW:** S10.5 is now a dedicated, mandatory workflow with user approval for each proposed guide change.

**⚠️ CRITICAL:** This is NOT optional. Every epic must run S10.5 to continuously improve guides.

**READ THE FULL GUIDE:**
```
stages/s10/s10_p1_guide_update_workflow.md
```

**Quick Overview of S10.5:**

1. **Analyze ALL lessons_learned.md files** (epic + all features)
2. **Identify guide gaps** for each lesson
3. **Create GUIDE_UPDATE_PROPOSAL.md** with prioritized proposals (P0-P3)
4. **Present each proposal to user** for individual approval
5. **Apply only approved changes** to guides
6. **Create separate commit** for guide updates
7. **Update guide_update_tracking.md** with applied lessons

**Priority System:**
- **P0 (Critical):** Prevents catastrophic bugs, mandatory gate gaps
- **P1 (High):** Significantly improves quality, reduces major rework
- **P2 (Medium):** Moderate improvements, clarifies ambiguity
- **P3 (Low):** Minor improvements, cosmetic fixes

**User Approval:**
- User reviews EACH proposal individually
- User can: Approve / Modify / Reject / Discuss
- Agent applies ONLY approved changes (or user modifications)
- No batch approvals or autonomous decisions

**Scope:**
- All files in `feature-updates/guides_v2/`
- `CLAUDE.md` (root project instructions)
- Anything supporting future agents

**Time Estimate:** 20-45 minutes (depends on number of lessons/proposals)

**Why this matters:**
- Continuous guide improvement based on real implementation experience
- Future agents benefit from lessons learned in THIS epic
- Systematic feedback loop: implementation → lessons → guide updates
- User has full control over guide evolution

**Transition to S10.5:**

Use the prompt from `prompts/guide_update_prompts.md`:

```
I'm reading `stages/s10/s10_p1_guide_update_workflow.md` to apply lessons learned to guides...

[Full prompt from guide_update_prompts.md - "Starting S10.5"]
```

**Exit Conditions:**
- [ ] Read stages/s10/s10_p1_guide_update_workflow.md (full guide)
- [ ] All lessons_learned.md files analyzed
- [ ] GUIDE_UPDATE_PROPOSAL.md created
- [ ] User reviewed all proposals individually
- [ ] Approved changes applied to guides
- [ ] Separate commit created for guide updates
- [ ] reference/guide_update_tracking.md updated
- [ ] guide-updates.txt updated (if applicable)
- [ ] Ready to proceed to STEP 5 (Final Commit)

**NEXT:** After S10.5 complete, proceed to STEP 5 (Final Commit) for epic code

---

### STEP 5: Final Commit

**Objective:** Commit all epic changes to git with clear, descriptive message.

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
# Stage modified files
git add {file1} {file2} {file3}

# Stage epic folder (all files)
git add feature-updates/{epic_name}/
```

**5c. Create Commit with Clear Message**

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

**5d. Verify Commit Successful**

Check git log:
```bash
git log -1 --stat
```

Verify commit message clear, all epic files included, file change counts reasonable.

**5e. Push Branch to Remote**

**CRITICAL:** Push the epic branch to remote for user review via Pull Request.

Push epic branch to remote:
```bash
git push origin {work_type}/KAI-{number}
```

**Example:**
```bash
git push origin epic/KAI-1
```

Verify push successful:
```bash
git status
```

**Expected:** "Your branch is up to date with 'origin/{work_type}/KAI-{number}'"

**5f. Create Pull Request**

**CRITICAL:** Create a Pull Request for user review instead of merging directly to main.

**Why Pull Requests?**
- ✅ User reviews all changes before merge
- ✅ GitHub UI provides best-in-class code review experience
- ✅ Can request changes if issues found
- ✅ GitHub Actions can run automated checks
- ✅ Clean git history with PR merge commits

**Create PR using GitHub CLI:**
```bash
gh pr create --base main --head {work_type}/KAI-{number} \
  --title "{commit_type}/KAI-{number}: Complete {epic_name} epic" \
  --body "$(cat <<'EOF'
## Epic Summary
{High-level description of epic from EPIC_README.md}

## Features Completed
- Feature 01: {feature_01_name}
- Feature 02: {feature_02_name}
- Feature 03: {feature_03_name}
{Continue for all features}

## Test Status
- Unit tests: {total}/{total} passing (100%)
- Epic smoke testing: PASSED (4/4 parts)
- Epic QC rounds: PASSED (3/3)
- User testing: PASSED (no bugs found)

## Files Changed
- {N} files changed
- {additions} insertions, {deletions} deletions

## Review Instructions
Please review this Pull Request using one of the following methods:

**Option 1: GitHub Web UI (Easiest)**
- Click "Files changed" tab to see all diffs
- Leave inline comments on specific lines if needed
- Click "Review changes" → "Approve" when satisfied
- Click "Merge pull request" to merge to main

**Option 2: VS Code Extension**
- Install "GitHub Pull Requests & Issues" extension
- Open PR in VS Code sidebar
- Review diffs in editor
- Approve and merge from VS Code

**Option 3: GitHub CLI**
- View diff: gh pr diff {number}
- Review: gh pr review {number} --approve
- Merge: gh pr merge {number}

**See:** feature-updates/USER_PR_REVIEW_GUIDE.md for detailed instructions

## Checklist Before Merging
- [ ] Review epic_smoke_test_plan.md results
- [ ] Review epic_lessons_learned.md
- [ ] Review code changes in GitHub PR diff view
- [ ] Verify all requirements from original {epic_name}.txt met
- [ ] All tests passing (100%)

🤖 Generated with Claude Code

Epic folder: feature-updates/KAI-{number}-{epic_name}/
EOF
)"
```

**Example:**
```bash
gh pr create --base main --head epic/KAI-1 \
  --title "feat/KAI-1: Complete improve_draft_helper epic" \
  --body "$(cat <<'EOF'
## Epic Summary
Improve draft helper with ADP integration, matchup system, and performance tracking.

## Features Completed
- Feature 01: ADP integration (market wisdom via Average Draft Position)
- Feature 02: Matchup system (opponent strength in projections)
- Feature 03: Performance tracking (accuracy vs projections)

## Test Status
- Unit tests: 2200/2200 passing (100%)
- Epic smoke testing: PASSED (4/4 parts)
- Epic QC rounds: PASSED (3/3)
- User testing: PASSED (no bugs found)

## Files Changed
- 15 files changed
- 847 insertions, 123 deletions

## Review Instructions
{... same as above ...}

## Checklist Before Merging
- [ ] Review epic_smoke_test_plan.md results
- [ ] Review epic_lessons_learned.md
- [ ] Review code changes in GitHub PR diff view
- [ ] Verify all requirements met
- [ ] All tests passing (100%)

🤖 Generated with Claude Code

Epic folder: feature-updates/KAI-1-improve_draft_helper/
EOF
)"
```

**PR Creation Output:**

The gh CLI will output the PR URL. Agent should:
1. Copy the PR URL
2. Present it to user with clear instructions

**Agent Output to User:**
```
✅ Pull Request created successfully!

PR URL: https://github.com/{owner}/{repo}/pull/{number}

Please review the Pull Request using your preferred method:

1. **GitHub Web UI** (Recommended for first-time)
   - Open PR URL in browser
   - Click "Files changed" tab
   - Review all diffs
   - Click "Approve" and "Merge" when satisfied

2. **VS Code Extension**
   - See USER_PR_REVIEW_GUIDE.md for setup instructions

3. **GitHub CLI**
   - gh pr view {number}
   - gh pr diff {number}
   - gh pr review {number} --approve
   - gh pr merge {number}

After you merge the PR, I'll update EPIC_TRACKER.md and move the epic to done/.
```

**Important Notes:**
- **Do NOT merge the PR yourself** - User must review and merge
- **Wait for user to merge** before proceeding to Step 5g
- **If user requests changes** - Make changes, push to same branch, PR auto-updates

**5g. Wait for User to Merge PR**

**CRITICAL:** Agent must wait for user to merge the PR before proceeding.

**After user merges PR:**
- User will say "I merged the PR" or similar
- Agent can then proceed to update EPIC_TRACKER.md (see 5h below)

**If user requests changes:**
1. User will leave comments on PR
2. Agent addresses comments
3. Agent commits fixes to same branch: `git push origin {work_type}/KAI-{number}`
4. PR automatically updates with new commits
5. User reviews again
6. Repeat until user approves and merges

**5h. Update EPIC_TRACKER.md (After User Merges PR)**

**IMPORTANT:** This step only happens AFTER user has merged the PR.

1. **Move epic from Active to Completed table**
2. **Increment "Next Available Number"**
3. **Add Epic Detail Section** with:
   - Epic description
   - Features implemented
   - Key changes
   - Commit history (use `git log --oneline --grep="KAI-{number}"`)
   - Testing results
   - Link to lessons learned

**Pull latest changes from main** (includes user's PR merge):
```bash
git checkout main
git pull origin main
```

**Commit EPIC_TRACKER.md update:**
```bash
git add feature-updates/EPIC_TRACKER.md
git commit -m "feat/KAI-{number}: Update EPIC_TRACKER with completed epic details"
git push origin main
```

**5i. Delete Epic Branch (Optional)**

```bash
git branch -d {work_type}/KAI-{number}
```

**Example:**
```bash
git branch -d epic/KAI-1
```

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
# Count directories in done/ (excluding guides_v2)
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

**IMPORTANT:** Do NOT move the original {epic_name}.txt file.

**Why:** Original request stays in feature-updates/ root for reference.

Verify:
```bash
ls feature-updates/{epic_name}.txt
```

**Expected:** File still exists in root.

---

### STEP 7: Final Verification & Completion

**Objective:** Verify epic cleanup complete and celebrate completion!

**Actions:**

**7a. Verify Epic in done/ Folder**

Confirm epic moved successfully:
```bash
ls feature-updates/done/
```

**7b. Verify Original Request Still in Root**

Confirm original request accessible:
```bash
ls feature-updates/{epic_name}.txt
```

**7c. Verify Git Shows Clean State**

Check git status:
```bash
git status
```

**Expected:** "Your branch is up to date with 'origin/main'", "nothing to commit, working tree clean" (or folder rename not staged - this is optional)

**7d. Update EPIC_README.md One Final Time**

Update the EPIC_README.md in done/ folder with epic completion summary.

**Reference:** See `STAGE_7_reference/epic_completion_template.md` for detailed template and instructions.

**Template:**
```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** S10 - Epic Cleanup
**Status:** ✅ COMPLETE

**Epic Completion Summary:**
- Start Date: {YYYY-MM-DD}
- End Date: {YYYY-MM-DD}
- Duration: {N} days
- Total Features: {N}
- Bug Fixes Created: {N}
- Final Test Pass Rate: 100% ({total_tests}/{total_tests} tests)

**Epic Moved To:** feature-updates/done/KAI-{N}-{epic_name}/
**Original Request:** feature-updates/{epic_name}.txt

**Next Steps:** None - epic complete! 🎉
```

**7e. Celebrate Epic Completion! 🎉**

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
- [ ] If bugs found: All fixed, S9 re-run from S9.P1, user re-tested
- [ ] Epic PR review passed (all categories)

### Git Commit and Pull Request
- [ ] All changes reviewed with git status and git diff
- [ ] All epic changes staged
- [ ] Commit created with clear, descriptive message
- [ ] Commit successful (verified with git log)
- [ ] Branch pushed to remote
- [ ] Pull Request created with epic summary
- [ ] User reviewed and merged PR
- [ ] EPIC_TRACKER.md updated (after PR merge)

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

**S10 - Epic Cleanup finalizes the epic and archives it for future reference:**

**Key Activities:**
1. Run unit tests (100% pass required)
2. Verify all documentation complete
3. Apply ALL lessons learned to guides (systematic search, 100% application)
4. Commit all changes to git with clear message
5. Push branch to remote and create Pull Request
6. Wait for user to review and merge PR
7. Update EPIC_TRACKER.md after PR merge
8. Move entire epic folder to done/ (max 10 epics, delete oldest if needed)
9. Leave original epic request in root for reference
10. Celebrate epic completion! 🎉

**Critical Success Factors:**
- 100% test pass rate before committing
- Complete documentation (README, lessons learned, test plan)
- ALL lessons applied (epic + features + bugfixes + debugging)
- User testing already passed in S9 Step 6 (prerequisite)
- Clear, descriptive commit message
- Entire epic folder moved (not individual features)
- Max 10 epics in done/ folder maintained

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
- `STAGE_7_reference/commit_message_examples.md` - Commit message format and examples
- `STAGE_7_reference/epic_completion_template.md` - EPIC_README.md completion template
- `STAGE_7_reference/lessons_learned_examples.md` - Lesson extraction and application guide
- `STAGE_7_ORIGINAL_BACKUP.md` - Original guide with all inline examples

---

**END OF STAGE 7 GUIDE**

---

**🎉 CONGRATULATIONS! 🎉**

If you've completed S10, you've successfully finished an entire epic from start to finish. The epic is now production-ready, fully tested (100% pass rate), thoroughly documented, and properly archived.

**Well done!**
