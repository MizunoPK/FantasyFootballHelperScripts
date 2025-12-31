# Epic Tracker

**Purpose:** Centralized log of all epics with KAI numbers, descriptions, and commit history.

**Branch Naming Convention:** `{work_type}/KAI-{number}`
- `epic` - Work with multiple features
- `feat` - Work with single feature
- `fix` - Bug fix work

**Commit Message Convention:** `{commit_type}/KAI-{number}: {message}`
- `feat` - Feature commit
- `fix` - Bug fix commit

---

## Active Epics

| KAI # | Epic Name | Type | Branch | Status | Date Started |
|-------|-----------|------|--------|--------|--------------|
| 1 | bug_fix-draft_mode | fix | fix/KAI-1 | In Progress | 2025-12-31 |

---

## Completed Epics

### Next Available Number: KAI-2

| KAI # | Epic Name | Type | Branch | Date Completed | Location |
|-------|-----------|------|--------|----------------|----------|
| - | - | - | - | - | - |

---

## Epic Details

<!-- Each epic gets a detailed section below once completed -->

---

## Usage Instructions

### Starting a New Epic

1. **Assign KAI Number:**
   - Check "Next Available Number" above
   - Use that number for your epic
   - Increment "Next Available Number" immediately

2. **Determine Work Type:**
   - `epic` - Multiple features (most common)
   - `feat` - Single feature only
   - `fix` - Already classified as bug fix

3. **Create Branch:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b {work_type}/KAI-{number}
   ```
   Example: `git checkout -b epic/KAI-1`

4. **Update Active Epics Table:**
   - Add row with KAI number, epic name, type, branch, status "In Progress", date

5. **During Development:**
   - All commits use format: `{commit_type}/KAI-{number}: {message}`
   - commit_type is either `feat` or `fix` (not `epic`)
   - Example: `feat/KAI-1: Add week 18 data folder creation`
   - Example: `fix/KAI-1: Correct week range validation logic`

### Completing an Epic

1. **Move from Active to Completed:**
   - Remove row from Active Epics table
   - Add row to Completed Epics table with completion date and done/ location

2. **Create Epic Detail Section:**
   - Add section below with full details (see template below)

3. **Update Next Available Number:**
   - Increment to next number

4. **Merge to Main:**
   ```bash
   git checkout main
   git pull origin main
   git merge {work_type}/KAI-{number}
   git push origin main
   ```

5. **Delete Branch (Optional):**
   ```bash
   git branch -d {work_type}/KAI-{number}
   ```

---

## Epic Detail Template

```markdown
---

### KAI-{number}: {Epic Name}

**Type:** epic / feat / fix
**Branch:** {work_type}/KAI-{number}
**Date Started:** YYYY-MM-DD
**Date Completed:** YYYY-MM-DD
**Location:** feature-updates/done/{epic_folder_name}/

**Description:**
{1-2 paragraph description of what this epic accomplished}

**Features Implemented:**
1. {feature_01_name} - {brief description}
2. {feature_02_name} - {brief description}
3. {feature_03_name} - {brief description}

**Key Changes:**
- {file_path}: {what changed and why}
- {file_path}: {what changed and why}
- {file_path}: {what changed and why}

**Commit History:**
- `{commit_hash}` - `{commit_type}/KAI-{number}: {commit message}`
- `{commit_hash}` - `{commit_type}/KAI-{number}: {commit message}`
- `{commit_hash}` - `{commit_type}/KAI-{number}: {commit message}`

**Testing Results:**
- Unit tests: {X}/{Y} passing
- Integration tests: {status}
- Epic smoke testing: {status}

**Lessons Learned:**
{Link to epic_lessons_learned.md or key insights}

**Related Documentation:**
- Epic README: feature-updates/done/{epic_name}/EPIC_README.md
- Epic Test Plan: feature-updates/done/{epic_name}/epic_smoke_test_plan.md
```

---

## Historical Notes

**Initialization:** 2025-12-31
- Tracker created to support git branching workflow
- Starting fresh with KAI-1 for next epic
- All future epics will be tracked here

---

## Quick Reference

**Current Next Number:** KAI-1

**Active Epic Count:** 0

**Completed Epic Count:** 0

**Branch Naming Examples:**
- `epic/KAI-1` - Multi-feature epic
- `feat/KAI-2` - Single feature work
- `fix/KAI-3` - Bug fix work

**Commit Message Examples:**
- `feat/KAI-1: Add ADP integration to PlayerManager`
- `feat/KAI-1: Create matchup difficulty calculation`
- `fix/KAI-1: Correct bye week penalty calculation`
- `fix/KAI-2: Fix draft mode crash when no players available`

---

**Last Updated:** 2025-12-31
