# STAGE 10: Epic Cleanup - Quick Reference Card

**Purpose:** One-page summary for final epic completion and archival
**Use Case:** Quick lookup when committing changes and archiving epic
**Total Time:** 85-130 minutes (includes S10.P1 guide updates)
**Note:** User testing completed in S9 (Step 6) before S10 begins

---

## Workflow Overview

```text
STEP 1: Pre-Cleanup Verification (5 min)
    ├─ Verify S9 complete
    ├─ Verify all features complete (S8.P2)
    ├─ Verify no pending work
    └─ Read epic_lessons_learned.md
    ↓
STEP 2: Run Unit Tests (5-10 min) ← MANDATORY GATE
    ├─ Execute: {TEST_COMMAND}
    ├─ Verify exit code 0 (all tests passing - 100%)
    └─ If ANY tests fail → Fix and re-run
    ↓
STEP 3: Documentation Verification (5-10 min)
    ├─ Verify EPIC_README.md complete
    ├─ Verify epic_lessons_learned.md contains insights
    ├─ Verify epic_smoke_test_plan.md accurate
    ├─ Verify all feature README.md files complete
    └─ Update any incomplete documentation
    ↓
STEP 4: Guide Update from Lessons Learned (20-45 min) ← S10.P1 MANDATORY
    ├─ Read stages/s10/s10_p1_guide_update_workflow.md (complete 9-step process)
    ├─ Analyze ALL lessons_learned.md files (epic + features)
    ├─ Create GUIDE_UPDATE_PROPOSAL.md (prioritized P0-P3)
    ├─ Present EACH proposal to user (individual approval)
    ├─ User decides: Approve / Modify / Reject / Discuss
    ├─ Apply only approved changes to guides
    ├─ Create separate commit for guide updates
    └─ Update guide_update_tracking.md
    ↓
STEP 5: Final Commit — Epic Implementation (5-10 min)
    ├─ Review changes (git status, git diff)
    ├─ Stage all epic-related changes
    └─ Create commit: "{commit_type}/SHAMT-{number}: {message}"
    ↓
STEP 6: Move Epic to done/ Folder (5 min)
    ├─ Create done/ folder if doesn't exist
    ├─ Clean up done/ (max 10 epics, delete oldest if needed)
    ├─ Move entire epic folder using git mv
    ├─ Verify move successful
    ├─ Leave original .txt in .shamt/epics/requests/
    └─ Commit the folder move
    ↓
STEP 7: Update .shamt/epics/EPIC_TRACKER.md (5 min)
    ├─ Move epic from Active to Completed table
    ├─ Add epic detail section
    ├─ Increment Next Available Number
    └─ Commit the EPIC_TRACKER.md update
    ↓
STEP 8: Push Branch and Create Pull Request (5 min)
    ├─ Verify working tree clean, then push all commits
    ├─ Create Pull Request using gh CLI
    ├─ Recommend squash commit message to user
    ├─ Wait for user to review and merge PR
    └─ Sync local main after merge
    ↓
STEP 9: Final Verification & Completion (5 min)
    ├─ Verify all commits pushed
    ├─ Verify PR created
    ├─ Verify git working tree clean
    └─ Epic COMPLETE! 🎉
```

---

## Step Summary Table

| Step | Duration | Key Activities | Mandatory Gate? |
|------|----------|----------------|-----------------|
| 1 | 5 min | Pre-cleanup verification | No |
| 2 | 5-10 min | Run unit tests (100% pass) | ✅ YES |
| 3 | 5-10 min | Documentation verification | No |
| 4 | 20-45 min | Guide updates (S10.P1, user approval) | No |
| 5 | 5-10 min | Final commit (epic implementation) | No |
| 6 | 5 min | Move epic to done/ folder (git mv + commit) | No |
| 7 | 5 min | Update .shamt/epics/EPIC_TRACKER.md + commit | No |
| 8 | 5 min | Push branch + create PR + wait for merge | No |
| 9 | 5 min | Final verification | No |

**Note:** User testing was moved to S9 (Step 6) - S10 only begins after user testing passes with zero bugs.

---

## Mandatory Gates (1 Required in S10)

**Note:** This is an S10-local gate (labeled S10-Gate-A to avoid conflict with global Gate 1 defined in reference/mandatory_gates.md).

### S10-Gate-A: Unit Tests - 100% Pass (Step 2)
**Location:** stages/s10/s10_epic_cleanup.md Step 2
**What it checks:**
- All unit tests passing
- Exit code = 0
- No test failures
- No skipped tests

**Pass Criteria:** 100% test pass rate
**If FAIL:** Fix failing tests, re-run until 100% pass

**Command:**
```bash
{TEST_COMMAND}
```

**Why mandatory:** Cannot commit code with failing tests

**Note:** User Testing (formerly Gate 2) has been moved to S9 (Step 6). S10 only begins after user testing passes with ZERO bugs.

---

## Prerequisites from S9

### User Testing Already Complete
**Location:** stages/s9/s9_p4_epic_final_review.md Step 6
**What was checked:**
- User tested complete system themselves
- User reported ZERO bugs
- All previous bugs fixed and S9 re-run

**Verified before S10:** User testing passed with ZERO bugs

**If bugs found in S9:**
- Create bug fixes (S2 → S5 → S6 → S7)
- RESTART S9 from S9.P1 (Epic Smoke Testing)
- Re-run all S9 steps (6a → S9.P2 → S9.P3)
- User re-tests in S9 Step 6
- Only proceed to S10 after user approval (ZERO bugs)

---

## Commit Message Format

### Required Format:
```json
{commit_type}/SHAMT-{number}: {message}

{body}
```

### Commit Type:
- `feat` - Feature work (most epic commits)
- `fix` - Bug fix work

**Note:** Use `feat` for epic commits (NOT `epic`, even for epic branches)

### Message:
- 100 characters or less
- Imperative mood ("Add", "Update", not "Added", "Updated")
- No emojis
- Brief summary of epic

### Body:
Three sections (Major features, Key changes, Testing):
- Keep concise (5-10 lines total)

### Example:
```text
feat/SHAMT-1: Add JSON export format and configurable output paths

Major features:
- Add JSON export alongside existing CSV export
- Support configurable output directory via CLI arg
- Add export history tracking

Key changes:
- data_exporter.py: Add JSON serialization support
- output_manager.py: Add configurable path handling

Testing:
- All unit tests passing ({N}/{N})
- Epic smoke testing passed
- Epic QC Validation Loop passed
```

---

## Git Workflow (Steps 5-8)

### Step 5: Epic Implementation Commit
```bash
git status       # Review all modified files
git diff         # Review all changes
git add .shamt/epics/SHAMT-{N}-{epic_name}/
git add <any other changed files>
git commit -m "{commit_type}/SHAMT-{number}: {message}"
```

### Step 6: Move Epic Folder and Commit
```bash
git mv .shamt/epics/SHAMT-{N}-{epic_name} .shamt/epics/done/SHAMT-{N}-{epic_name}
git commit -m "chore/SHAMT-{N}: Move completed epic to done/ folder"
```

### Step 7: Update EPIC_TRACKER and Commit
```bash
# Edit .shamt/epics/EPIC_TRACKER.md (move epic to Completed, add details, increment number)
git add .shamt/epics/EPIC_TRACKER.md
git commit -m "chore/SHAMT-{N}: Update EPIC_TRACKER with completed epic"
```

### Step 8: Push Branch and Create Pull Request
```bash
git status       # Verify working tree clean
git push origin {work_type}/SHAMT-{number}
gh pr create --base main --head {work_type}/SHAMT-{number} \
  --title "{commit_type}/SHAMT-{number}: Complete {epic_name} epic" \
  --body "{Epic summary, features, tests, review instructions}"
# Recommend squash commit message to user, then wait for merge
# After merge:
git checkout main && git fetch origin && git reset --hard origin/main
```

---

## Critical Rules Summary

- ✅ S9 MUST be complete before S10
- ✅ Run unit tests BEFORE committing (100% pass required)
- ✅ Verify ALL documentation complete
- ✅ User testing completed in S9 (Step 6) — S10 begins only after user reports ZERO bugs
- ✅ Commit message must use new format ({commit_type}/SHAMT-{number})
- ✅ Push branch and create PR for user review
- ✅ Wait for user to review and merge PR
- ✅ Update .shamt/epics/EPIC_TRACKER.md in Step 7 (before creating PR in Step 8)
- ✅ Move ENTIRE epic folder (not individual features)
- ✅ Update CLAUDE.md if guides improved
- ✅ Verify epic is TRULY complete

---

## Common Pitfalls

### ❌ Pitfall 1: Starting S10 Before User Testing Passes
**Problem:** "All unit tests pass, I'll proceed to S10 commit"
**Impact:** User finds bugs after commit, rework required
**Solution:** User testing is completed in S9 Step 6 (ZERO bugs required). S10 only begins after S9 is fully complete.

### ❌ Pitfall 2: Committing with Failing Tests
**Problem:** "I'll fix the tests later"
**Impact:** Broken code in git history, tests always fail
**Solution:** 100% test pass BEFORE commit (Step 2 gate)

### ❌ Pitfall 3: Not Applying Lessons Learned
**Problem:** "I'll skip updating guides, the lessons are documented"
**Impact:** Future agents repeat same mistakes, guides don't improve
**Solution:** Apply ALL lessons from ALL sources (Step 4, 100% application)

### ❌ Pitfall 4: Committing with Bugs from User Testing
**Problem:** "User found a small bug, I'll commit and fix later"
**Impact:** Known bugs in production, tech debt
**Solution:** Fix ALL bugs → RESTART S9 → Get ZERO bugs from user

### ❌ Pitfall 5: Vague Commit Message
**Problem:** "feat/SHAMT-1: Add features"
**Impact:** Git history unclear, future agents can't understand changes
**Solution:** Descriptive message (100 chars), list major features in body

### ❌ Pitfall 6: Moving Individual Features
**Problem:** "I'll move each feature folder separately"
**Impact:** Epic split across locations, hard to find complete epic
**Solution:** Move ENTIRE epic folder at once

### ❌ Pitfall 7: Not Updating .shamt/epics/EPIC_TRACKER.md
**Problem:** "I'll update EPIC_TRACKER later"
**Impact:** Active epics list out of date, SHAMT number conflicts
**Solution:** Update .shamt/epics/EPIC_TRACKER.md in Step 7 (before creating PR in Step 8)

---

## Quick Checklist: "Am I Ready for Next Step?"

**Before Step 1:**
- [ ] S9 complete (EPIC_README.md shows ✅)
- [ ] No pending features or bug fixes
- [ ] Ready to start epic cleanup

**Step 1 → Step 2:**
- [ ] S9 verified complete
- [ ] All features verified complete (S8.P2)
- [ ] No pending work found
- [ ] epic_lessons_learned.md reviewed

**Step 2 → Step 3:**
- [ ] Unit tests executed
- [ ] Exit code = 0 (100% pass)
- [ ] No failing tests
- [ ] No skipped tests

**Step 3 → Step 4:**
- [ ] EPIC_README.md verified complete
- [ ] epic_lessons_learned.md verified complete
- [ ] epic_smoke_test_plan.md verified accurate
- [ ] All feature README.md files verified complete

**Step 4 → Step 5:**
- [ ] ALL lessons_learned.md files found (epic + features + bugfixes)
- [ ] Proposals created and individually approved by user
- [ ] Approved changes applied to guides
- [ ] Separate commit created for guide updates
- [ ] guide_update_tracking.md updated

**Step 5 → Step 6:**
- [ ] git status and git diff reviewed
- [ ] All epic-related changes staged
- [ ] Epic implementation commit created with clear message
- [ ] Commit verified (git log)

**Step 6 → Step 7:**
- [ ] done/ folder exists (created if needed)
- [ ] done/ cleaned up (max 10 epics maintained)
- [ ] Entire epic folder moved using git mv
- [ ] Move verified (folder structure intact)
- [ ] Original .txt still in .shamt/epics/requests/
- [ ] Folder move committed

**Step 7 → Step 8:**
- [ ] Epic moved from Active to Completed in EPIC_TRACKER.md
- [ ] Epic detail section added
- [ ] Next Available Number incremented
- [ ] EPIC_TRACKER.md update committed

**Step 8 → Step 9:**
- [ ] Working tree clean (git status)
- [ ] All commits pushed to remote branch
- [ ] Pull Request created
- [ ] Squash commit message recommended to user
- [ ] User reviewed and merged PR
- [ ] Local main synced (git reset --hard origin/main)

**Step 9 → Complete:**
- [ ] Epic visible in done/ folder (post-merge)
- [ ] Git working tree clean
- [ ] Epic COMPLETE!

---

## File Outputs

**Step 4:**
- Updated guide files (in .shamt/guides/)
- GUIDE_UPDATE_PROPOSAL.md (in epic folder)
- Updated guide_update_tracking.md

**Step 5:**
- Git commit (epic implementation work)

**Step 6:**
- `.shamt/epics/done/SHAMT-{N}-{epic_name}/` (entire epic folder moved via git mv)
- `.shamt/epics/requests/{epic_name}.txt` (original request, stays in place)
- Git commit (epic folder move)

**Step 7:**
- Updated .shamt/epics/EPIC_TRACKER.md (epic moved to Completed, number incremented)
- Git commit (.shamt/epics/EPIC_TRACKER.md update)

**Step 8:**
- Remote branch with all commits pushed
- Pull Request created for user review

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting S10 | stages/s10/s10_epic_cleanup.md |
| Commit message format | reference/stage_10/commit_message_examples.md |
| Epic completion format | reference/stage_10/epic_completion_template.md |
| Lessons learned examples | reference/stage_10/lessons_learned_examples.md |

---

## Exit Conditions

**S10 is complete when:**
- [ ] All 9 steps complete (1-9)
- [ ] Pre-cleanup verification passed
- [ ] Unit tests passed (100%)
- [ ] Documentation verified complete
- [ ] Guides updated via S10.P1 (user-approved proposals applied)
- [ ] Epic implementation commit created
- [ ] Epic folder moved to done/ (git mv + committed)
- [ ] .shamt/epics/EPIC_TRACKER.md updated and committed
- [ ] All commits pushed to remote branch
- [ ] Pull Request created and merged by user
- [ ] Local main synced
- [ ] Git clean state
- [ ] Epic COMPLETE and archived!

**Next Stage:** None (Epic complete - celebration time! 🎉)

---

**Last Updated:** 2026-02-21
