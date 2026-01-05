# STAGE 7: Epic Cleanup - Quick Reference Card

**Purpose:** One-page summary for final epic completion and archival
**Use Case:** Quick lookup when committing changes, testing with user, and archiving epic
**Total Time:** 15-30 minutes (+ user testing time)

---

## Workflow Overview

```
STEP 1: Pre-Cleanup Verification (5 min)
    ├─ Verify Stage 6 complete
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
STEP 4: Update Guides (10-20 min)
    ├─ Find ALL lessons_learned.md files (epic + features + bugfixes)
    ├─ Extract lessons from EACH file
    ├─ Create master checklist of ALL proposed guide updates
    ├─ Apply EACH lesson to guides (100% application required)
    └─ Update CLAUDE.md if workflow changed
    ↓
STEP 5: User Testing & Bug Fix Protocol (Variable) ← MANDATORY GATE
    ├─ Ask user to test complete system themselves
    ├─ User reports any bugs discovered
    ├─ If bugs found → Follow bug fix protocol (Stage 2→5a→5b→5c)
    ├─ After bug fixes → RESTART Stage 6 (Epic Final QC)
    └─ Return to Stage 7 only when user testing passes with ZERO bugs
    ↓
STEP 6: Final Commit (5-10 min)
    ├─ Review changes (git status, git diff)
    ├─ Stage all epic-related changes
    ├─ Create commit: "{commit_type}/KAI-{number}: {message}"
    ├─ Merge branch to main (git merge)
    ├─ Push to origin (git push)
    └─ Update EPIC_TRACKER.md
    ↓
STEP 7: Move Epic to done/ Folder (2 min)
    ├─ Create done/ folder if doesn't exist
    ├─ Move entire epic folder: mv {epic}/ done/{epic}/
    ├─ Verify move successful
    └─ Leave original epic request (.txt) in root
    ↓
STEP 8: Final Verification & Completion (2 min)
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
| 4 | 10-20 min | Update guides (apply lessons) | No |
| 5 | Variable | User testing (ZERO bugs) | ✅ YES |
| 6 | 5-10 min | Final commit, merge, push | No |
| 7 | 2 min | Move epic to done/ | No |
| 8 | 2 min | Final verification | No |

---

## Mandatory Gates (2 Required)

### Gate 1: Unit Tests - 100% Pass (Step 2)
**Location:** stages/stage_7/epic_cleanup.md Step 2
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

### Gate 2: User Testing - ZERO Bugs (Step 5)
**Location:** stages/stage_7/epic_cleanup.md Step 5
**What it checks:**
- User tests complete system themselves
- User reports any bugs found
- All bugs fixed before commit

**Pass Criteria:** User testing passes with ZERO bugs
**If FAIL:** Create bug fixes → RESTART Stage 6 → Return to Step 5 → Repeat until ZERO bugs

**Why mandatory:** User must validate epic works as expected before archival

---

## Bug Fix Protocol During User Testing

### If User Finds Bugs:

**1. DO NOT commit with bugs**
   - User testing is MANDATORY before commit
   - Cannot proceed with known bugs

**2. Create bug fixes:**
   - Use bug fix workflow (Stage 2 → 5a → 5b → 5c)
   - High priority bug fixes (blocks epic completion)

**3. RESTART Stage 6:**
   - After ALL bug fixes complete
   - COMPLETE restart from Stage 6a (Epic Smoke Testing)
   - Re-run all steps (6a → 6b → 6c)

**4. Return to Step 5:**
   - Ask user to test again
   - Repeat until ZERO bugs

**5. ONLY THEN proceed to Step 6:**
   - User approval obtained
   - ZERO bugs remaining
   - Ready to commit

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
git add feature-updates/{epic_name}/
git add <any other changed files>
```

### 6.3: Commit
```bash
git commit -m "{commit_type}/KAI-{number}: {message}"
```

### 6.4: Merge to Main
```bash
git checkout main
git pull origin main
git merge {work_type}/KAI-{number}
```

### 6.5: Push to Origin
```bash
git push origin main
```

### 6.6: Update EPIC_TRACKER.md
- Move epic from Active to Completed table
- Add epic detail section
- Increment "Next Available Number"
- Commit and push EPIC_TRACKER.md

---

## Critical Rules Summary

- ✅ Stage 6 MUST be complete before Stage 7
- ✅ Run unit tests BEFORE committing (100% pass required)
- ✅ Verify ALL documentation complete
- ✅ User testing is MANDATORY (BEFORE commit)
- ✅ Commit message must use new format ({commit_type}/KAI-{number})
- ✅ Merge branch to main AFTER commit
- ✅ Update EPIC_TRACKER.md AFTER merge
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
**Solution:** Fix ALL bugs → RESTART Stage 6 → Get ZERO bugs from user

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
- [ ] Stage 6 complete (EPIC_README.md shows ✅)
- [ ] No pending features or bug fixes
- [ ] Ready to start epic cleanup

**Step 1 → Step 2:**
- [ ] Stage 6 verified complete
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
- [ ] If bugs found: Bug fixes complete + Stage 6 restarted
- [ ] User approval obtained
- [ ] Ready to commit

**Step 6 → Step 7:**
- [ ] All changes committed
- [ ] Branch merged to main
- [ ] Pushed to origin
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
- `feature-updates/done/{epic_name}/` (entire epic folder moved)
- `feature-updates/{epic_name}.txt` (original request, stays in root)

**Step 8:**
- Final EPIC_README.md with completion summary

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting Stage 7 | stages/stage_7/epic_cleanup.md |
| Commit message format | reference/stage_7/commit_message_examples.md |
| Epic completion format | reference/stage_7/epic_completion_template.md |
| Lessons learned examples | reference/stage_7/lessons_learned_examples.md |

---

## Exit Conditions

**Stage 7 is complete when:**
- [ ] All 8 steps complete (1-8)
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
