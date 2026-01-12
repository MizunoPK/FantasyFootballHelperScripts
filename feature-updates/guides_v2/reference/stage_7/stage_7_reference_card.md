# STAGE 7: Epic Cleanup - Quick Reference Card

**Purpose:** One-page summary for final epic completion and archival
**Use Case:** Quick lookup when committing changes and archiving epic
**Total Time:** 40-80 minutes (includes S10.P1 guide updates)
**Note:** User testing completed in Stage 9 (Step 6) before Stage 10 begins

---

## Workflow Overview

```
STEP 1: Pre-Cleanup Verification (5 min)
    ├─ Verify Stage 9 complete
    ├─ Verify all features complete (Stage 5e)
    ├─ Verify no pending work
    └─ Read epic_lessons_learned.md
    ↓
STEP 2: Run Unit Tests (5-10 min) ← MANDATORY GATE
    ├─ Execute: python tests/run_all_tests.py
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
    ├─ Read guide_update_workflow.md (complete 9-step process)
    ├─ Analyze ALL lessons_learned.md files (epic + features)
    ├─ Create GUIDE_UPDATE_PROPOSAL.md (prioritized P0-P3)
    ├─ Present EACH proposal to user (individual approval)
    ├─ User decides: Approve / Modify / Reject / Discuss
    ├─ Apply only approved changes to guides
    ├─ Create separate commit for guide updates
    └─ Update guide_update_tracking.md
    ↓
STEP 5: Final Commit & Pull Request (5-10 min)
    ├─ Review changes (git status, git diff)
    ├─ Stage all epic-related changes
    ├─ Create commit: "{commit_type}/KAI-{number}: {message}"
    ├─ Push branch to remote (git push origin {work_type}/KAI-{number})
    ├─ Create Pull Request using gh CLI
    ├─ Wait for user to review and merge PR
    └─ Update EPIC_TRACKER.md after user merges
    ↓
STEP 6: Move Epic to done/ Folder (2 min)
    ├─ Create done/ folder if doesn't exist
    ├─ Move entire epic folder: mv {epic}/ done/{epic}/
    ├─ Verify move successful
    └─ Leave original epic request (.txt) in root
    ↓
STEP 7: Final Verification & Completion (2 min)
    ├─ Verify epic in done/ folder
    ├─ Verify git clean state
    ├─ Update EPIC_README.md with completion summary
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
| 5 | 5-10 min | Final commit, create PR, merge | No |
| 6 | 2 min | Move epic to done/ | No |
| 7 | 2 min | Final verification | No |

**Note:** User testing was moved to Stage 9 (Step 6) - Stage 10 only begins after user testing passes with zero bugs.

---

## Mandatory Gates (1 Required in Stage 10)

### Gate 1: Unit Tests - 100% Pass (Step 2)
**Location:** stages/s10/s7_epic_cleanup.md Step 2
**What it checks:**
- All unit tests passing
- Exit code = 0
- No test failures
- No skipped tests

**Pass Criteria:** 100% test pass rate
**If FAIL:** Fix failing tests, re-run until 100% pass

**Command:**
```bash
python tests/run_all_tests.py
```

**Why mandatory:** Cannot commit code with failing tests

**Note:** User Testing (formerly Gate 2) has been moved to Stage 9 (Step 6). Stage 10 only begins after user testing passes with ZERO bugs.

---

## Prerequisites from Stage 9

### User Testing Already Complete
**Location:** stages/s9/s6_p4_epic_final_review.md Step 6
**What was checked:**
- User tested complete system themselves
- User reported ZERO bugs
- All previous bugs fixed and Stage 9 re-run

**Verified before Stage 10:** User testing passed with ZERO bugs

**If bugs found in Stage 9:**
- Create bug fixes (Stage 2 → 5a → 5b → 5c)
- RESTART Stage 9 from 6a (Epic Smoke Testing)
- Re-run all Stage 9 steps (6a → 6b → 6c)
- User re-tests in Stage 9 Step 6
- Only proceed to Stage 10 after user approval (ZERO bugs)

---

## Commit Message Format

### Required Format:
```
{commit_type}/KAI-{number}: {message}

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
- List major features implemented
- List major changes made
- Keep concise (5-10 lines)

### Example:
```
feat/KAI-1: Add ADP integration and projection system to draft helper

Major features:
- Integrate ADP data from FantasyPros API
- Add injury assessment to player projections
- Implement schedule strength analysis
- Update recommendation engine with new multipliers

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## Git Workflow (Step 6)

### 6.1: Review Changes
```bash
git status       # See all modified files
git diff         # See all changes
```

### 6.2: Stage Changes
```bash
git add feature-updates/KAI-{N}-{epic_name}/
git add <any other changed files>
```

### 6.3: Commit
```bash
git commit -m "{commit_type}/KAI-{number}: {message}"
```

### 6.4: Push Branch to Remote
```bash
git push origin {work_type}/KAI-{number}
```

### 6.5: Create Pull Request
```bash
gh pr create --base main --head {work_type}/KAI-{number} \
  --title "{commit_type}/KAI-{number}: Complete {epic_name} epic" \
  --body "{Epic summary, features, tests, review instructions}"
```

See USER_PR_REVIEW_GUIDE.md for user review options.

### 6.6: Wait for User to Merge PR
Agent waits for user to review and merge the Pull Request in GitHub.

### 6.7: Update EPIC_TRACKER.md (After User Merges)
- Pull latest: git checkout main && git pull origin main
- Move epic from Active to Completed table
- Add epic detail section
- Increment "Next Available Number"
- Commit and push EPIC_TRACKER.md

---

## Critical Rules Summary

- ✅ Stage 9 MUST be complete before Stage 10
- ✅ Run unit tests BEFORE committing (100% pass required)
- ✅ Verify ALL documentation complete
- ✅ User testing is MANDATORY (BEFORE commit)
- ✅ Commit message must use new format ({commit_type}/KAI-{number})
- ✅ Push branch and create PR for user review
- ✅ Wait for user to review and merge PR
- ✅ Update EPIC_TRACKER.md AFTER user merges
- ✅ Move ENTIRE epic folder (not individual features)
- ✅ Update CLAUDE.md if guides improved
- ✅ Verify epic is TRULY complete

---

## Common Pitfalls

### ❌ Pitfall 1: Skipping User Testing
**Problem:** "All tests pass, I'll skip user testing"
**Impact:** User finds bugs in production, rework required
**Solution:** User testing is MANDATORY (Step 5), cannot skip

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
**Solution:** Fix ALL bugs → RESTART Stage 9 → Get ZERO bugs from user

### ❌ Pitfall 5: Vague Commit Message
**Problem:** "feat/KAI-1: Add features"
**Impact:** Git history unclear, future agents can't understand changes
**Solution:** Descriptive message (100 chars), list major features in body

### ❌ Pitfall 6: Moving Individual Features
**Problem:** "I'll move each feature folder separately"
**Impact:** Epic split across locations, hard to find complete epic
**Solution:** Move ENTIRE epic folder at once

### ❌ Pitfall 7: Not Updating EPIC_TRACKER.md
**Problem:** "I'll update EPIC_TRACKER later"
**Impact:** Active epics list out of date, KAI number conflicts
**Solution:** Update EPIC_TRACKER.md immediately after merge (Step 6.6)

---

## Quick Checklist: "Am I Ready for Next Step?"

**Before Step 1:**
- [ ] Stage 9 complete (EPIC_README.md shows ✅)
- [ ] No pending features or bug fixes
- [ ] Ready to start epic cleanup

**Step 1 → Step 2:**
- [ ] Stage 9 verified complete
- [ ] All features verified complete (Stage 5e)
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
- [ ] Lessons extracted from EACH file
- [ ] Master checklist created
- [ ] ALL lessons applied to guides (100%)
- [ ] CLAUDE.md updated (if workflow changed)

**Step 5 → Step 6:**
- [ ] User tested complete system
- [ ] User testing passed with ZERO bugs
- [ ] If bugs found: Bug fixes complete + Stage 9 restarted
- [ ] User approval obtained
- [ ] Ready to commit

**Step 6 → Step 7:**
- [ ] All changes committed
- [ ] Branch pushed to remote
- [ ] Pull Request created for user review
- [ ] User has merged PR to main
- [ ] EPIC_TRACKER.md updated

**Step 7 → Step 8:**
- [ ] Epic folder moved to done/
- [ ] Move successful (verified)
- [ ] Original .txt file still in root

**Step 8 → Complete:**
- [ ] Epic verified in done/ folder
- [ ] Git clean state verified
- [ ] EPIC_README.md updated with completion summary
- [ ] Epic COMPLETE!

---

## File Outputs

**Step 4:**
- Updated guide files (in guides_v2/)
- Updated CLAUDE.md (if workflow changed)

**Step 6:**
- Git commit (with epic changes)
- Updated EPIC_TRACKER.md
- Git history shows epic completion

**Step 7:**
- `feature-updates/done/KAI-{N}-{epic_name}/` (entire epic folder moved)
- `feature-updates/{epic_name}.txt` (original request, stays in root)

**Step 8:**
- Final EPIC_README.md with completion summary

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting Stage 10 | stages/s10/s7_epic_cleanup.md |
| Commit message format | reference/stage_7/commit_message_examples.md |
| Epic completion format | reference/stage_7/epic_completion_template.md |
| Lessons learned examples | reference/stage_7/lessons_learned_examples.md |

---

## Exit Conditions

**Stage 10 is complete when:**
- [ ] All 7 steps complete (1-7)
- [ ] Pre-cleanup verification passed
- [ ] Unit tests passed (100%)
- [ ] Documentation verified complete
- [ ] Guides updated (all lessons applied)
- [ ] User testing passed (ZERO bugs)
- [ ] Final commit created and pushed
- [ ] EPIC_TRACKER.md updated
- [ ] Epic folder moved to done/
- [ ] Git clean state
- [ ] Epic COMPLETE and archived!

**Next Stage:** None (Epic complete - celebration time! 🎉)

---

**Last Updated:** 2026-01-04
