# Git Branching Workflow

This document describes the git branching workflow for epic development in the Fantasy Football Helper Scripts project.

**Key Principle:** All epic work must be done on feature branches (not directly on main).

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

**Step 3: Assign KAI number**
- Check `feature-updates/EPIC_TRACKER.md` for next available number
- Update EPIC_TRACKER.md with new epic in "Active Epics" table

**Step 4: Determine work type**
- `epic` - Work with multiple features (most epics)
- `feat` - Work with single feature only
- `fix` - Bug fix work

**Step 5: Create and checkout branch**
```bash
git checkout -b {work_type}/KAI-{number}
```

**Examples:**
```bash
git checkout -b epic/KAI-1  # Multi-feature epic
git checkout -b feat/KAI-2  # Single feature work
git checkout -b fix/KAI-3   # Bug fix work
```

---

### During Epic Work (Stages 1-6)

**Branch Rules:**
- All work happens on the epic branch
- Stay on branch until S10 (Epic Cleanup)
- Do not merge back to main until user approves PR

**Commit Format:**
```bash
{commit_type}/KAI-{number}: {message}
```

**Important:** `commit_type` is either `feat` or `fix` (NOT `epic`)

**Commit Types:**
- `feat` - Feature-related commits (new functionality)
- `fix` - Bug fix commits

**Examples:**
```bash
git commit -m "feat/KAI-1: Add ADP integration to PlayerManager"
git commit -m "feat/KAI-1: Implement draft helper recommendations"
git commit -m "fix/KAI-1: Fix player name validation in draft mode"
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
git commit -m "feat/KAI-1: Complete improve_draft_helper epic"
```

**Step 2: Push branch to remote**
```bash
git push origin {work_type}/KAI-{number}
```

**Example:**
```bash
git push origin epic/KAI-1
```

**Step 3: Create Pull Request for user review**
```bash
gh pr create --base main --head {work_type}/KAI-{number} \
  --title "{commit_type}/KAI-{number}: Complete {epic_name} epic" \
  --body "{Epic summary with features, tests, review instructions}"
```

**Example:**
```bash
gh pr create --base main --head epic/KAI-1 \
  --title "feat/KAI-1: Complete improve_draft_helper epic" \
  --body "$(cat <<'EOF'
- Epic: improve_draft_helper

## Features Implemented
- Feature 01: ADP integration for player recommendations
- Feature 02: Confidence scoring for draft suggestions
- Feature 03: Top 200 player filtering

## Testing
- 100% unit test pass rate (2,256 tests passing)
- Epic smoke testing complete (all scenarios pass)
- User testing complete (zero bugs reported)

## Review Instructions
1. Review feature changes in league_helper/draft_helper.py
2. Check updated tests in tests/league_helper/test_draft_helper.py
3. Run: python tests/run_all_tests.py
4. Test draft helper: python run_league_helper.py (select Draft Helper mode)
EOF
)"
```

**Step 4: User reviews and merges PR**
- User reviews PR in GitHub UI, VS Code extension, or CLI
- User approves and merges when satisfied
- See `feature-updates/USER_PR_REVIEW_GUIDE.md` for review options

**Step 5: Update EPIC_TRACKER.md** (after user merges PR)
```bash
- Switch back to main and pull merged changes
git checkout main
git pull origin main

- Update EPIC_TRACKER.md:
- - Move epic from "Active" to "Completed" table
- - Add epic detail section with commits
- - Increment "Next Available Number"

- Commit the tracker update
git add feature-updates/EPIC_TRACKER.md
git commit -m "docs: Update EPIC_TRACKER.md after KAI-1 completion"
git push origin main
```

**Step 6: Delete branch (optional)**
```bash
git branch -d {work_type}/KAI-{number}
git push origin --delete {work_type}/KAI-{number}
```

---

## Naming Conventions

### Branch Naming

**Format:** `{work_type}/KAI-{number}`

**Examples:**
- `epic/KAI-1` - Multi-feature epic
- `feat/KAI-2` - Single feature
- `fix/KAI-3` - Bug fix

**Rules:**
- Work type tracked in EPIC_TRACKER.md
- KAI number is unique per epic
- All features within an epic share the same KAI number

---

### Epic Folder Naming

**Format:** `feature-updates/KAI-{N}-{epic_name}/`

**Examples:**
- `feature-updates/KAI-1-improve_draft_helper/`
- `feature-updates/KAI-3-integrate_new_player_data_into_simulation/`

**Original Request File:** `feature-updates/{epic_name}.txt` (no KAI number)

**Why include KAI number:**
- Ensures unique folder names
- Matches branch naming convention
- Enables quick identification of epic
- Links folder to EPIC_TRACKER.md entry

---

### Commit Message Convention

**Format:** `{commit_type}/KAI-{number}: {message}`

**Examples:**
```bash
feat/KAI-1: Add ADP integration to PlayerManager
feat/KAI-1: Implement confidence scoring algorithm
fix/KAI-1: Fix null pointer in player validation
```

**Rules:**
- Brief and descriptive (100 characters or less)
- No emojis
- Imperative mood ("Add" not "Added", "Fix" not "Fixed")
- All features in epic use same KAI number
- commit_type is `feat` or `fix` (not `epic`)
- No AI attribution (no "Co-Authored-By" lines, no "Generated with" footers, no AI credit)

**Commit Body (optional but recommended):**
```bash
git commit -m "feat/KAI-1: Add ADP integration to PlayerManager" -m "
- Integrate ADP data from player-data-fetcher
- Add get_player_by_adp() method
- Update recommendation algorithm to use ADP
- Add 15 unit tests for ADP functionality
"
```

---

## EPIC_TRACKER.md Management

**Location:** `feature-updates/EPIC_TRACKER.md`

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

**Answer:** Yes. All features within an epic use the same branch (`epic/KAI-{number}`). Features are committed individually after S7 S10.P3, but all commits go to the same epic branch.

**Example:**
```bash
git checkout -b epic/KAI-1
- Work on feature 01
git commit -m "feat/KAI-1: Complete feature 01 - ADP integration"
- Work on feature 02
git commit -m "feat/KAI-1: Complete feature 02 - confidence scoring"
- Work on feature 03
git commit -m "feat/KAI-1: Complete feature 03 - top 200 filtering"
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
git checkout -b fix/KAI-{new-number}

- Fix the bug
git commit -m "fix/KAI-{new-number}: Fix critical bug in player scoring"

- Create PR for hotfix
gh pr create --base main --head fix/KAI-{new-number} ...

- Return to epic work
git checkout epic/KAI-{epic-number}
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
git checkout epic/KAI-{number}
git rebase main

- Resolve conflicts if any
- ... fix conflicts ...
git add .
git rebase --continue

- Force push (required after rebase)
git push origin epic/KAI-{number} --force-with-lease
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
- Commit during planning stages (1-4)
- Commit mid-implementation (5a-5b)
- Commit before testing passes (5c smoke testing/QC)

---

### Commit Messages

**✅ DO:**
- Use imperative mood ("Add" not "Added")
- Be specific ("Fix null pointer in player validation" not "Fix bug")
- Reference KAI number in every commit
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
- Create branches without KAI numbers
- Leave stale branches after epic completion
- Merge without user approval

---

## Troubleshooting

### Problem: "Branch already exists"

**Cause:** You already created this branch

**Solution:**
```bash
- Check if branch exists
git branch -a | grep KAI-{number}

- If it exists, checkout instead of creating
git checkout epic/KAI-{number}
```

---

### Problem: "Detached HEAD state"

**Cause:** Checked out a commit instead of a branch

**Solution:**
```bash
- Create branch from current state
git checkout -b epic/KAI-{number}
```

---

### Problem: "Failed to push"

**Cause:** Remote branch has changes you don't have locally

**Solution:**
```bash
- Pull with rebase
git pull --rebase origin epic/KAI-{number}

- Push
git push origin epic/KAI-{number}
```

---

## See Also

- `feature-updates/EPIC_TRACKER.md` - Epic tracking and KAI number assignment
- `feature-updates/USER_PR_REVIEW_GUIDE.md` - PR review options for users
- `CLAUDE.md` - Complete epic development workflow
- `feature-updates/guides_v2/stages/s10/s10_epic_cleanup.md` - S10 guide (includes PR creation)
