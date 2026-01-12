# STAGE 1: Epic Planning - Quick Reference Card

**Purpose:** One-page summary for epic initialization and feature breakdown
**Use Case:** Quick lookup when starting a new epic or verifying setup steps
**Total Time:** 45-75 minutes (includes user validation)

---

## Workflow Overview

```
PHASE 1: Initial Setup (15-20 min)
    ├─ Step 1.0: Create Git Branch (BEFORE any changes)
    │   ├─ Verify on main, pull latest
    │   ├─ Assign KAI number from EPIC_TRACKER.md
    │   ├─ Create branch: {work_type}/KAI-{number}
    │   └─ Update EPIC_TRACKER.md and commit immediately
    ├─ Step 1.1: Create epic folder
    ├─ Step 1.2: Move {epic_name}.txt into epic folder
    └─ Step 1.3: Create EPIC_README.md with Agent Status
    ↓
PHASE 2: Epic Analysis (10-15 min)
    ├─ Read epic request thoroughly
    ├─ Identify goals, constraints, requirements
    └─ Conduct broad codebase reconnaissance
    ↓
PHASE 3: Feature Breakdown Proposal (15-30 min)
    ├─ Identify major components/subsystems
    ├─ Propose feature list with justification
    ├─ Present to user for approval
    ├─ WAIT for user confirmation/modifications
    ├─ Create epic ticket (outcome validation) ← USER VALIDATION
    └─ WAIT for user approval of epic ticket
    ↓
PHASE 4: Epic Structure Creation (10-15 min)
    ├─ Create feature folders (per approved breakdown)
    ├─ Create epic_smoke_test_plan.md (PLACEHOLDER - mark as "INITIAL")
    ├─ Create epic_lessons_learned.md
    ├─ Create research/ folder (shared across features)
    ├─ Create GUIDE_ANCHOR.md (resumption instructions)
    └─ Update EPIC_README.md with Epic Progress Tracker
    ↓
PHASE 5: Transition to Stage 2 (5 min)
    ├─ Mark Stage 1 complete in EPIC_README.md
    ├─ Update Agent Status (next: Stage 2)
    └─ Announce transition to user
```

---

## Phase Summary Table

| Phase | Duration | Key Activities | User Interaction | Gate? |
|-------|----------|----------------|------------------|-------|
| 1 | 15-20 min | Git branch, epic folder, EPIC_README.md | None | No |
| 2 | 10-15 min | Read epic, reconnaissance | None | No |
| 3 | 15-30 min | Propose features, create epic ticket | Feature approval, epic ticket validation | ✅ YES |
| 4 | 10-15 min | Create feature folders, test plan, research folder | None | No |
| 5 | 5 min | Mark complete, transition to Stage 2 | None | No |

---

## Mandatory Gates

### Gate 1: Feature Breakdown Approval (Phase 3)
**Location:** stages/s1/s1_epic_planning.md Phase 3
**What it checks:**
- User approves proposed feature list
- Feature breakdown makes sense
- Each feature has clear purpose (1-2 sentences)

**Pass Criteria:** User explicitly confirms feature breakdown
**If FAIL:** User provides feedback, agent revises breakdown, re-proposes

### Gate 2: Epic Ticket Validation (Phase 3)
**Location:** stages/s1/s1_epic_planning.md Steps 3.6-3.7
**What it checks:**
- Epic ticket accurately reflects user's desired outcomes
- Agent understanding validated
- Epic ticket becomes immutable reference (like epic notes)

**Pass Criteria:** User approves epic ticket
**If FAIL:** User corrects misunderstandings, agent updates epic ticket, re-validates

---

## Decision Points

### Decision 1: Determine Work Type (Step 1.0d)
**When:** Creating git branch
**Options:**
- `epic` - Work with multiple features (most epics)
- `feat` - Work with single feature only
- `fix` - Bug fix work

**How to decide:** Most multi-feature work uses `epic`
**Impact:** Determines branch name format and EPIC_TRACKER classification

### Decision 2: Feature Count (Phase 3)
**When:** Proposing feature breakdown
**Options:**
- Propose FEWER features (safer - can add during Stage 2 discovery)
- Propose MORE features (harder to merge features later)

**How to decide:** If unsure, propose fewer features
**Impact:** Epic structure is set after folder creation

### Decision 3: Feature Naming (Phase 4)
**When:** Creating feature folders
**Options:**
- Descriptive names (recommended): `feature_01_player_integration`
- Generic names (avoid): `feature_01_utilities`, `feature_01_misc`

**How to decide:** Each feature must have distinct value (1-2 sentence purpose)
**Impact:** Feature names appear in progress tracking, git commits, documentation

---

## Critical Rules Summary

- ✅ Create git branch BEFORE any changes (Step 1.0)
- ✅ User MUST approve feature breakdown before epic ticket
- ✅ Create epic ticket and get user validation (Steps 3.6-3.7)
- ✅ Create GUIDE_ANCHOR.md in epic folder (resumption instructions)
- ✅ epic_smoke_test_plan.md is PLACEHOLDER (mark "INITIAL - WILL UPDATE")
- ✅ Update EPIC_README.md Agent Status after each major step
- ✅ Feature numbering: feature_01_{name}, feature_02_{name} (zero-padded)
- ✅ Create research/ folder in epic root (shared across features)
- ✅ Epic planning does NOT include deep dives (Stage 2 handles that)
- ✅ If unsure about breakdown, propose FEWER features
- ✅ Every feature MUST have clear purpose (avoid "miscellaneous")
- ✅ Mark completion in EPIC_README.md before Stage 2

---

## Common Pitfalls

### ❌ Pitfall 1: Making Changes Before Creating Branch
**Problem:** Creating epic folder on main branch
**Impact:** Pollutes main branch, difficult rollback, merge conflicts
**Solution:** Create git branch FIRST (Step 1.0), THEN create folders

### ❌ Pitfall 2: Skipping Epic Ticket Validation
**Problem:** Assuming you understand epic without validation
**Impact:** Build wrong thing, rework in Stage 5c or user testing
**Solution:** Create epic ticket (Step 3.6), get user validation (Step 3.7)

### ❌ Pitfall 3: Creating "Miscellaneous" Features
**Problem:** Grouping unrelated items into "utilities" or "misc" feature
**Impact:** Feature scope unclear, difficult testing, poor cohesion
**Solution:** Each feature has distinct value and clear purpose

### ❌ Pitfall 4: Too Many Features
**Problem:** Breaking epic into 10+ small features
**Impact:** Overhead managing features, Stage 2/3/4 takes too long
**Solution:** Aim for 2-5 features, combine related functionality

### ❌ Pitfall 5: Detailed Test Plan in Stage 1
**Problem:** Writing specific test scenarios before deep dives
**Impact:** Test plan based on assumptions, will need rewrite
**Solution:** Stage 1 test plan is PLACEHOLDER, mark "INITIAL - WILL UPDATE"

### ❌ Pitfall 6: Not Updating EPIC_TRACKER.md
**Problem:** Skipping EPIC_TRACKER.md update or committing later
**Impact:** KAI number conflicts, no tracking in git history
**Solution:** Update EPIC_TRACKER.md and commit IMMEDIATELY after branch creation

### ❌ Pitfall 7: Starting Deep Dives in Stage 1
**Problem:** Trying to flesh out feature specs during epic planning
**Impact:** Stage 1 takes hours instead of minutes, premature decisions
**Solution:** Stage 1 = structure only, Stage 2 = deep dives (separate stage)

---

## Quick Checklist: "Am I Ready for Next Phase?"

**Phase 1 → Phase 2:**
- [ ] Git branch created: {work_type}/KAI-{number}
- [ ] EPIC_TRACKER.md updated and committed
- [ ] Epic folder created: `feature-updates/KAI-{N}-{epic_name}/`
- [ ] {epic_name}.txt moved into epic folder
- [ ] EPIC_README.md created with Agent Status

**Phase 2 → Phase 3:**
- [ ] Epic request read thoroughly
- [ ] Goals, constraints, requirements identified
- [ ] Broad codebase reconnaissance complete
- [ ] Ready to propose feature breakdown

**Phase 3 → Phase 4:**
- [ ] Feature breakdown proposed to user
- [ ] User approved feature breakdown
- [ ] Epic ticket created with desired outcomes
- [ ] User validated epic ticket

**Phase 4 → Phase 5:**
- [ ] Feature folders created (matching approved breakdown)
- [ ] epic_smoke_test_plan.md created (marked as "INITIAL - WILL UPDATE")
- [ ] epic_lessons_learned.md created
- [ ] research/ folder created
- [ ] GUIDE_ANCHOR.md created
- [ ] EPIC_README.md updated with Epic Progress Tracker

**Phase 5 → Stage 2:**
- [ ] Stage 1 marked complete in EPIC_README.md
- [ ] Agent Status updated (next: Stage 2)
- [ ] User informed of transition

---

## File Outputs

**Phase 1:**
- Git branch: `{work_type}/KAI-{number}`
- EPIC_TRACKER.md (updated and committed)
- `feature-updates/KAI-{N}-{epic_name}/` folder
- `KAI-{N}-{epic_name}/{epic_name}_notes.txt` (moved from root)
- `KAI-{N}-{epic_name}/EPIC_README.md`

**Phase 3:**
- Epic ticket in conversation (user-validated)

**Phase 4:**
- `KAI-{N}-{epic_name}/feature_01_{name}/` (and feature_02, feature_03, etc.)
- `KAI-{N}-{epic_name}/epic_smoke_test_plan.md` (PLACEHOLDER)
- `KAI-{N}-{epic_name}/epic_lessons_learned.md`
- `KAI-{N}-{epic_name}/research/`
- `KAI-{N}-{epic_name}/GUIDE_ANCHOR.md`
- EPIC_README.md updated with Epic Progress Tracker

---

## Git Branch Workflow

**Branch Naming:** `{work_type}/KAI-{number}`
**Examples:**
- `epic/KAI-1` - Multi-feature epic
- `feat/KAI-2` - Single feature
- `fix/KAI-3` - Bug fix

**Commit Message Format:** `{commit_type}/KAI-{number}: {message}`
**Examples:**
- `feat/KAI-1: Initialize epic tracking for improve_draft_helper`
- `feat/KAI-1: Create epic folder structure with 3 features`

**Notes:**
- `work_type` can be epic/feat/fix (in branch name)
- `commit_type` is always feat or fix (NOT epic, even for epic branches)
- All commits in epic use same KAI number

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting a new epic | stages/s1/s1_epic_planning.md |
| Need git workflow details | CLAUDE.md (Git Branching Workflow section) |
| Need folder structure templates | templates/TEMPLATES_INDEX.md |

---

## Exit Conditions

**Stage 1 is complete when:**
- [ ] Git branch created and EPIC_TRACKER.md updated
- [ ] Epic folder structure complete
- [ ] Feature breakdown user-approved
- [ ] Epic ticket user-validated
- [ ] All feature folders created
- [ ] Placeholder test plan created
- [ ] EPIC_README.md shows Stage 1 complete
- [ ] Ready to start Stage 2 (feature deep dives)

**Next Stage:** Stage 2 (Feature Deep Dive) - for each feature in sequence

---

**Last Updated:** 2026-01-04
