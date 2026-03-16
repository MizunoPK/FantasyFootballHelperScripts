# Git Branching Workflow

This document describes the git branching workflow for epic development in the SHAMT project.

**Key Principle:** All epic work must be done on feature branches (not directly on main).

---

## Table of Contents

1. [Branch Management](#branch-management)
2. [Naming Conventions](#naming-conventions)
3. [.shamt/epics/EPIC_TRACKER.md Management](#shamtepicsepic_trackermd-management)
4. [Common Scenarios](#common-scenarios)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [See Also](#see-also)

---

## Branch Management

### When Starting an Epic (S1)

**Step 1: Verify you're on main**
```bash
git checkout main
```

**Step 2: Pull latest changes**
```bash
git pull origin main
```

**Step 3: Assign SHAMT number**
- Check `.shamt/epics/EPIC_TRACKER.md` for next available number
- Update .shamt/epics/EPIC_TRACKER.md with new epic in "Active Epics" table

**Step 4: Determine work type**
- `epic` - Work with multiple features (most epics)
- `feat` - Work with single feature only
- `fix` - Bug fix work

**Step 5: Create and checkout branch**
```bash
git checkout -b {work_type}/SHAMT-{number}
```

**Examples:**
```bash
git checkout -b epic/SHAMT-1  # Multi-feature epic
git checkout -b feat/SHAMT-2  # Single feature work
git checkout -b fix/SHAMT-3   # Bug fix work
```

---

### During Epic Work (Stages 1-6)

**Branch Rules:**
- All work happens on the epic branch
- Stay on branch until S10 (Epic Cleanup)
- Do not merge back to main until user approves PR

**Commit Format:**
```bash
{commit_type}/SHAMT-{number}: {message}
```

**Important:** `commit_type` is either `feat` or `fix` (NOT `epic`)

**Commit Types:**
- `feat` - Feature-related commits (new functionality)
- `fix` - Bug fix commits

**Examples:**
```bash
git commit -m "feat/SHAMT-1: Add Rank integration to RecordManager"
git commit -m "feat/SHAMT-1: Implement recommendation engine recommendations"
git commit -m "fix/SHAMT-1: Fix item name validation in draft mode"
```

**When to Commit:**
- After S7 S10.P3 (Feature completed, reviewed, tested)
- After S10 cleanup (Epic completed, ready for PR)
- Not during Stages 1-4 (planning only)
- Not during S5-S6 (implementation in progress)

---

### When Completing an Epic (S10)

**Step 1: Commit changes on branch** (after user testing passes)
```bash
git add .
git commit -m "feat/SHAMT-1: Complete improve_recommendation_engine epic"
```

**Step 2: Push branch to remote**
```bash
git push origin {work_type}/SHAMT-{number}
```

**Example:**
```bash
git push origin epic/SHAMT-1
```

**Step 3: Create Pull Request for user review**
```bash
gh pr create --base main --head {work_type}/SHAMT-{number} \
  --title "{commit_type}/SHAMT-{number}: Complete {epic_name} epic" \
  --body "{Epic summary with features, tests, review instructions}"
```

**Example:**
```bash
gh pr create --base main --head epic/SHAMT-1 \
  --title "feat/SHAMT-1: Complete improve_recommendation_engine epic" \
  --body "$(cat <<'EOF'
- Epic: improve_recommendation_engine

## Features Implemented
- Feature 01: Rank-based scoring integration
- Feature 02: Confidence scoring for recommendations
- Feature 03: Top-N item filtering

## Testing
- 100% unit test pass rate ({N} tests passing)
- Epic smoke testing complete (all scenarios pass)
- User testing complete (zero bugs reported)

## Review Instructions
1. Review feature changes in [module]/recommendation_engine.py
2. Check updated tests in tests/[module]/test_recommendation_engine.py
3. Run: {TEST_COMMAND}
4. Test recommendation engine: python run_[module].py (select Draft Helper mode)
EOF
)"
```

**Step 4: User reviews and merges PR**
- User reviews PR in GitHub UI, VS Code extension, or CLI
- User approves and merges when satisfied

**Step 5: Update .shamt/epics/EPIC_TRACKER.md** (after user merges PR)
```bash
- Switch back to main and pull merged changes
git checkout main
git pull origin main

- Update .shamt/epics/EPIC_TRACKER.md:
- - Move epic from "Active" to "Completed" table
- - Add epic detail section with commits
- - Increment "Next Available Number"

- Commit the tracker update
git add .shamt/epics/EPIC_TRACKER.md
git commit -m "docs: Update .shamt/epics/EPIC_TRACKER.md after SHAMT-1 completion"
git push origin main
```

**Step 6: Delete branch (optional)**
```bash
git branch -d {work_type}/SHAMT-{number}
git push origin --delete {work_type}/SHAMT-{number}
```

---

## Naming Conventions

### Branch Naming

**Format:** `{work_type}/SHAMT-{number}`

**Examples:**
- `epic/SHAMT-1` - Multi-feature epic
- `feat/SHAMT-2` - Single feature
- `fix/SHAMT-3` - Bug fix

**Rules:**
- Work type tracked in .shamt/epics/EPIC_TRACKER.md
- SHAMT number is unique per epic
- All features within an epic share the same SHAMT number

---

### Epic Folder Naming

**Format:** `.shamt/epics/SHAMT-{N}-{epic_name}/`

**Examples:**
- `.shamt/epics/SHAMT-1-add_dark_mode_to_cli/`
- `.shamt/epics/SHAMT-3-add_json_export_format/`

**Original Request File:** `.shamt/epics/requests/{epic_name}.txt` (no SHAMT number)

**Why include SHAMT number:**
- Ensures unique folder names
- Matches branch naming convention
- Enables quick identification of epic
- Links folder to .shamt/epics/EPIC_TRACKER.md entry

---

### Commit Message Convention

**Format:** `{commit_type}/SHAMT-{number}: {message}`

**Examples:**
```bash
feat/SHAMT-1: Add Rank integration to RecordManager
feat/SHAMT-1: Implement confidence [domain algorithm]
fix/SHAMT-1: Fix null pointer in item validation
```

**Rules:**
- Brief and descriptive (100 characters or less)
- No emojis
- Imperative mood ("Add" not "Added", "Fix" not "Fixed")
- All features in epic use same SHAMT number
- commit_type is `feat` or `fix` (not `epic`)
- No AI attribution (no "Co-Authored-By" lines, no "Generated with" footers, no AI credit)

**Commit Body (optional but recommended):**
```bash
git commit -m "feat/SHAMT-1: Add Rank integration to RecordManager" -m "
- Integrate rank data from [data-fetcher]
- Add get_item_by_rank() method
- Update recommendation algorithm to use rank priority
- Add 15 unit tests for rank priority functionality
"
```

---

## .shamt/epics/EPIC_TRACKER.md Management

**Location:** `.shamt/epics/EPIC_TRACKER.md`

**Updates Required:**

### S1: Starting Epic
- Add epic to "Active Epics" table
- Increment "Next Available Number"
- Document epic name, features, start date

### S10: Completing Epic
- Move epic from "Active" to "Completed" table
- Add epic detail section with:
  - All commits (with hashes)
  - Features implemented
  - Files changed
  - Test results

### After Commits (for documentation)
- Track commits for inclusion in epic detail section
- Document significant changes

---

## Common Scenarios

### Scenario: Multiple Features in Epic

**Question:** Do all features in an epic use the same branch?

**Answer:** Yes. All features within an epic use the same branch (`epic/SHAMT-{number}`). Features are committed individually after S7 S10.P3, but all commits go to the same epic branch.

**Example:**
```bash
git checkout -b epic/SHAMT-1
- Work on feature 01
git commit -m "feat/SHAMT-1: Complete feature 01 - Rank integration"
- Work on feature 02
git commit -m "feat/SHAMT-1: Complete feature 02 - confidence scoring"
- Work on feature 03
git commit -m "feat/SHAMT-1: Complete feature 03 - top 200 filtering"
- S10: Create PR for entire epic
```

---

### Scenario: Hotfix During Epic

**Question:** What if I need to fix a bug in main while working on an epic?

**Answer:** Create a separate fix branch from main:

```bash
- Save epic work
git stash

- Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b fix/SHAMT-{new-number}

- Fix the bug
git commit -m "fix/SHAMT-{new-number}: Fix critical bug in item scoring"

- Create PR for hotfix
gh pr create --base main --head fix/SHAMT-{new-number} ...

- Return to epic work
git checkout epic/SHAMT-{epic-number}
git stash pop
```

---

### Scenario: Branch Conflicts

**Question:** What if my epic branch conflicts with main?

**Answer:** Rebase your epic branch onto main:

```bash
- Update main
git checkout main
git pull origin main

- Rebase epic branch
git checkout epic/SHAMT-{number}
git rebase main

- Resolve conflicts if any
- ... fix conflicts ...
git add .
git rebase --continue

- Force push (required after rebase)
git push origin epic/SHAMT-{number} --force-with-lease
```

**⚠️ Warning:** Only force push if you haven't shared the branch with others.

---

## Best Practices

### Commit Frequency

**✅ DO:**
- Commit after each feature completes S7 S10.P3
- Commit after S10 cleanup completes
- Commit with meaningful messages

**❌ DON'T:**
- Commit during planning stages (S1-S3)
- Commit mid-implementation (S5-S6)
- Commit before testing passes (S7 smoke testing/QC)

---

### Commit Messages

**✅ DO:**
- Use imperative mood ("Add" not "Added")
- Be specific ("Fix null pointer in item validation" not "Fix bug")
- Reference SHAMT number in every commit
- Keep first line under 100 characters

**❌ DON'T:**
- Use vague messages ("Update code", "Fix stuff")
- Include emojis or subjective prefixes
- Include AI attribution (no "Co-Authored-By" lines, no "Generated with" footers, no AI credit)
- Commit without running tests first
- Mix multiple unrelated changes in one commit

---

### Branch Hygiene

**✅ DO:**
- Delete branches after merging to main
- Keep branch names consistent with convention
- Rebase onto main before creating PR
- Squash commits if PR review requests it

**❌ DON'T:**
- Commit directly to main
- Create branches without SHAMT numbers
- Leave stale branches after epic completion
- Merge without user approval

---

## Troubleshooting

### Problem: "Branch already exists"

**Cause:** You already created this branch

**Solution:**
```bash
- Check if branch exists
git branch -a | grep SHAMT-{number}

- If it exists, checkout instead of creating
git checkout epic/SHAMT-{number}
```

---

### Problem: "Detached HEAD state"

**Cause:** Checked out a commit instead of a branch

**Solution:**
```bash
- Create branch from current state
git checkout -b epic/SHAMT-{number}
```

---

### Problem: "Failed to push"

**Cause:** Remote branch has changes you don't have locally

**Solution:**
```bash
- Pull with rebase
git pull --rebase origin epic/SHAMT-{number}

- Push
git push origin epic/SHAMT-{number}
```

---

## See Also

- `.shamt/epics/EPIC_TRACKER.md` - Epic tracking and SHAMT number assignment
- `CLAUDE.md` - Complete epic development workflow
- `.shamt/guides/stages/s10/s10_epic_cleanup.md` - S10 guide (includes PR creation)
