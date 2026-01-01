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
| - | - | - | - | - | - |

---

## Completed Epics

### Next Available Number: KAI-2

| KAI # | Epic Name | Type | Branch | Date Completed | Location |
|-------|-----------|------|--------|----------------|----------|
| 1 | bug_fix-draft_mode | fix | fix/KAI-1 | 2025-12-31 | feature-updates/done/bug_fix-draft_mode/ |

---

## Epic Details

<!-- Each epic gets a detailed section below once completed -->

---

### KAI-1: bug_fix-draft_mode

**Type:** fix
**Branch:** fix/KAI-1
**Date Started:** 2025-12-31
**Date Completed:** 2025-12-31
**Location:** feature-updates/done/bug_fix-draft_mode/

**Description:**
Fixed critical bug in Add to Roster mode where RB/WR players could only match FLEX-ideal draft rounds, not their native position rounds (RB-ideal, WR-ideal). This caused 8 out of 15 roster slots to incorrectly display as [EMPTY SLOT] even with a full roster. The fix allows FLEX-eligible positions (RB/WR) to match both their native position rounds AND FLEX rounds, while maintaining exact-match-only behavior for non-FLEX positions (QB/TE/K/DST).

**Features Implemented:**
1. feature_01_fix_player_round_assignment - Created `_position_matches_ideal()` helper method to correctly handle FLEX position matching logic

**Key Changes:**
- league_helper/add_to_roster_mode/AddToRosterModeManager.py: Added `_position_matches_ideal()` helper method (30 lines) to replace buggy inline logic
- league_helper/add_to_roster_mode/AddToRosterModeManager.py: Updated `_match_players_to_rounds()` to use new helper method instead of `get_position_with_flex()`
- tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py: Added 7 comprehensive tests validating bug fix and preventing regressions

**Commit History:**
- `cf20b90` - `feat/KAI-1: Initialize epic tracking for bug_fix-draft_mode`
- `13b4fe4` - `fix/KAI-1: Fix Add to Roster mode player-to-round assignment logic`

**Testing Results:**
- Unit tests: 2,423/2,423 passing (100%)
- Epic smoke testing: Passed (3/3 applicable parts)
- Epic QC rounds: Passed (3/3 rounds, 0 issues)
- User testing: Passed (zero bugs found)

**Lessons Learned:**
See feature-updates/done/bug_fix-draft_mode/epic_lessons_learned.md - Key success factors: rigorous Stage 5a planning (24 iterations with Algorithm Traceability Matrix), comprehensive testing (7 unit tests + integration test with actual user data), data values verification (real player names, not placeholders), progressive quality validation (6 QC rounds total), and zero tech debt tolerance.

**Related Documentation:**
- Epic README: feature-updates/done/bug_fix-draft_mode/EPIC_README.md
- Epic Test Plan: feature-updates/done/bug_fix-draft_mode/epic_smoke_test_plan.md
- Epic Lessons Learned: feature-updates/done/bug_fix-draft_mode/epic_lessons_learned.md

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
