# PHASE 1: Issue Discovery & Checklist Update

**Purpose:** Create/update ISSUES_CHECKLIST.md with discovered issues

**When to Use:** QC/Smoke Testing discovers issues that need to be tracked and resolved

**Previous Phase:** None (entry point from testing)

**Next Phase:** PHASE 2 (Investigation) - See `debugging/investigation.md`

---

## Triggered When

- Smoke Testing (S7.P1) Part 3 discovers issues
- QC Rounds (S7.P2) any round discovers issues
- Epic Smoke Testing (S9.P1) discovers issues
- Epic QC Rounds (S9.P2) discovers issues
- User Testing (S9.P3) discovers bugs

---

## Actions

### Step 1: Create debugging/ folder if it doesn't exist

```bash
# For feature-level (issues found during feature testing)
mkdir -p feature_XX_name/debugging/diagnostic_logs

# For epic-level (issues found during epic testing or user testing)
mkdir -p epic_name/debugging/diagnostic_logs
```markdown

**Decision: Feature vs Epic?**
- **Feature-level:** Issues discovered during S7.P1 or S7.P2 for a specific feature
- **Epic-level:** Issues discovered during S9 (Epic Testing) or S10 (User Testing)

---

### Step 2: Create or update ISSUES_CHECKLIST.md

**If first issue for this feature/epic:**
- Create new ISSUES_CHECKLIST.md using template below

**If subsequent issues:**
- Open existing ISSUES_CHECKLIST.md
- Add new issues to the Issues table
- Update counts

---

### Step 3: Add issues discovered during testing

**For each issue found:**

1. **Assign a number:** Next sequential number in checklist

2. **Create descriptive name:**
   - Format: `{problem_area}_{symptom}`
   - Examples: "player_scoring_returns_null", "projection_calculation_wrong", "integration_data_mismatch"

3. **Set initial status:** 🔴 NOT_STARTED

4. **Record discovery location:**
   - Examples: "Smoke Part 3", "QC Round 1", "Epic Smoke Step 2", "User Testing"

5. **Add any immediate notes:**
   - Error messages
   - Affected components
   - Relationship to other issues

---

### Step 4: Update README Agent Status

**Feature-level (in feature_XX_name/README.md):**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}

**Current Phase:** DEBUGGING_PROTOCOL
**Current Guide:** debugging/discovery.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Testing Stage Paused:** {S7.P1 Smoke Part 3 / S7.P2 QC Round 1 / S9.P1 Epic Smoke / S9.P2 Epic QC / etc}

**Debugging Status:**
- Issues in Checklist: {count}
- Fixed (User Confirmed): 0
- In Progress: 0
- Not Started: {count}

**Next Action:** Begin investigation of Issue #1 (read debugging/investigation.md)

**Critical Rules from Guide:**
- Issue checklist workflow (ISSUES_CHECKLIST.md always current)
- Loop back to testing after all issues resolved
- User verification required for each issue
```markdown

**Epic-level (in epic_name/EPIC_README.md):**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}

**Current Phase:** DEBUGGING_PROTOCOL
**Current Guide:** debugging/discovery.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Testing Stage Paused:** {S9.P1 Epic Smoke Step 2 / S9.P2 Epic QC Round 1 / S10 User Testing}

**Debugging Status:**
- Issues in Checklist: {count}
- Fixed (User Confirmed): 0
- In Progress: 0
- Not Started: {count}

**Next Action:** Begin investigation of Issue #1 (read debugging/investigation.md)

**Critical Rules from Guide:**
- Epic-level debugging folder (epic_name/debugging/)
- Loop back to S9.P1 after all issues resolved
- User verification required for each issue
```markdown

---

## Template: debugging/ISSUES_CHECKLIST.md

```markdown
# Issues Checklist - {Feature/Epic Name}

**Source:** {Feature/Epic}
**Testing Stage:** {S7.P1 Smoke Testing / S7.P2 QC Rounds / S9.P1 Epic Smoke Testing / S9.P2 Epic QC Rounds / S9.P3 User Testing}
**Created:** {YYYY-MM-DD HH:MM}
**Status:** In Progress

---

## Issue Status Legend

- 🔴 NOT_STARTED - Not yet investigated
- 🟡 INVESTIGATING - Currently in investigation rounds
- 🟠 SOLUTION_READY - Fix implemented, needs user verification
- 🟢 FIXED - User confirmed resolution
- ⚪ BLOCKED - Waiting on external dependency
- 🔵 DUPLICATE - Duplicate of another issue

---

## Issues

| # | Issue Name | Status | Phase | User Confirmed? | Discovered During | Notes |
|---|------------|--------|-------|-----------------|-------------------|-------|
| 1 | player_scoring_returns_null | 🔴 NOT_STARTED | - | ❌ NO | Smoke Part 3 | E2E test failed |
| 2 | projection_values_incorrect | 🔴 NOT_STARTED | - | ❌ NO | Smoke Part 3 | Off by ~5 points |

---

## Current Focus

**Active Issue:** None (starting with Issue #1)
**Current Phase:** Phase 1 (Issue Discovery)
**Next Action:** Begin investigation of Issue #1 (create issue_01_player_scoring_returns_null.md)

---

## Loop-Back Status

**Testing Stage to Loop Back To:** {S7.P1 Step 1 / S9.P1 Step 1}
**Reason:** Must re-run {smoke/QC} tests from beginning after fixes

---

## Completed Issues Summary

{Empty initially - will populate as issues are resolved}

---

## Investigation Statistics

**Total Issues:** {count}
**Fixed (User Confirmed):** 0
**In Progress:** 0
**Blocked:** 0

**Average Investigation Rounds:** N/A (no issues completed yet)
**Total Debugging Time:** {will track}
```markdown

---

## New Issue Discovery During Debugging

**What if you discover a NEW issue WHILE debugging another issue?**

### Immediate Actions

1. **Add to ISSUES_CHECKLIST.md immediately:**
   ```markdown
   | 3 | new_issue_name | 🔴 NOT_STARTED | - | ❌ NO | Discovered during Issue #1 | Related to Issue #1 |
   ```markdown

2. **Update current issue's file:**
   ```markdown
   ## Related Issues

   - Issue #3: {name} - Discovered during Investigation Round 2
   ```markdown

3. **Assess blocking relationship:**

**Decision tree:**
```text
Does Issue #3 BLOCK Issue #1?
├─ YES (cannot fix #1 without fixing #3 first)
│  ├─ Update ISSUES_CHECKLIST.md "Current Focus" to Issue #3
│  ├─ Update Issue #1 status: ⚪ BLOCKED (blocked by Issue #3)
│  ├─ Update Issue #3 status: 🟡 INVESTIGATING
│  └─ Begin investigating Issue #3
│
└─ NO (can fix #1 independently)
   ├─ Note relationship in ISSUES_CHECKLIST.md
   ├─ Continue with Issue #1
   └─ Will investigate Issue #3 after #1 is resolved
```markdown

4. **Ask user if priority should change:**

```markdown
I discovered a new issue while investigating Issue #{current}:

**New Issue:** {name}
**Description:** {brief description}
**Relationship:** {how it relates to current issue}

**Blocking Relationship:**
- Does Issue #{new} BLOCK Issue #{current}? {YES/NO}
- If YES: Should I switch focus to #{new} first?

**Recommendation:** {your assessment}

What would you like me to do?
```markdown

---

## Feature-Level vs Epic-Level Folder Structure

### Feature-Level Debugging

**Location:** `feature_XX_name/debugging/`

**When to use:**
- Issues discovered during S7.P1 for THIS feature
- Issues discovered during S7.P2 for THIS feature
- Issues specific to one feature's implementation

**Folder structure:**
```text
feature_01_player_integration/
└── debugging/
    ├── ISSUES_CHECKLIST.md
    ├── investigation_rounds.md
    ├── issue_01_{name}.md
    ├── issue_02_{name}.md
    ├── lessons_learned.md
    └── diagnostic_logs/
        ├── issue_01_round1.log
        └── issue_02_round1.log
```markdown

**Loop-back destination:** S7.P1 Step 1 (Smoke Testing)

---

### Epic-Level Debugging

**Location:** `epic_name/debugging/`

**When to use:**
- Issues discovered during S9.P1 (Epic Smoke Testing)
- Issues discovered during S9.P2 (Epic QC Rounds)
- Issues discovered during S10 (User Testing)
- Cross-feature integration issues
- Epic-level coordination issues

**Folder structure:**
```text
epic_name/
└── debugging/
    ├── ISSUES_CHECKLIST.md
    ├── investigation_rounds.md
    ├── issue_01_{name}.md
    ├── issue_02_{name}.md
    ├── lessons_learned.md
    └── diagnostic_logs/
        ├── issue_01_round1.log
        └── issue_02_round1.log
```

**Loop-back destination:** S9.P1 Step 1 (Epic Smoke Testing)

---

## Common Scenarios

### Scenario 1: First Issue Found During Smoke Part 3

**Actions:**
1. Create `feature_XX_name/debugging/` folder
2. Create `feature_XX_name/debugging/diagnostic_logs/` folder
3. Create `ISSUES_CHECKLIST.md` using template
4. Add issue to table
5. Update feature README Agent Status
6. Next: Read `debugging/investigation.md` for PHASE 2

---

### Scenario 2: Multiple Issues Found During Same Test

**Actions:**
1. If first issue: Create debugging/ folder and checklist
2. Add ALL issues to ISSUES_CHECKLIST.md at once
3. Prioritize (usually address in order discovered)
4. Update README Agent Status with total count
5. Next: Read `debugging/investigation.md` to begin with Issue #1

---

### Scenario 3: New Issue Found During QC (After Some Issues Already Fixed)

**Actions:**
1. Open existing `debugging/ISSUES_CHECKLIST.md`
2. Add new issue to table (next sequential number)
3. Update counts
4. Update README Agent Status
5. Finish current investigation if in progress
6. Then investigate new issue

---

### Scenario 4: User Reports Bugs During S10 Testing

**Actions:**
1. Create `epic_name/debugging/` folder (if doesn't exist)
2. Create/update `epic_name/debugging/ISSUES_CHECKLIST.md`
3. Add ALL user-reported bugs to checklist
4. Set "Discovered During" to "User Testing (S10)"
5. Update EPIC_README Agent Status
6. Inform user you're entering debugging protocol
7. After all bugs fixed: Loop back to S9.P1 (NOT S10)
   - **Why?** Fixes might affect epic-level integration
   - Must re-validate epic smoke and QC before user tests again

---

## Next Steps

**After completing PHASE 1 (Issue Discovery & Checklist Update):**

✅ ISSUES_CHECKLIST.md created/updated
✅ All discovered issues added to table
✅ README Agent Status updated
✅ Folder structure created

**Next:** Read `debugging/investigation.md` for PHASE 2 (Investigation)

---

**END OF PHASE 1 GUIDE**
