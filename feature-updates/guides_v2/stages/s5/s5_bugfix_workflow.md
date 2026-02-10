# STAGE 5: Bug Fix Workflow Guide (V2)

**Purpose:** Handle bugs or missing scope discovered during epic implementation with a streamlined workflow that minimizes disruption to ongoing feature work.

**When to Use:** Bug discovered during S5 (feature implementation) or reported by user

---


## Table of Contents

1. [🚨 MANDATORY READING PROTOCOL](#-mandatory-reading-protocol)
2. [Prerequisites](#prerequisites)
3. [Overview](#overview)
4. [🛑 Critical Rules](#-critical-rules)
5. [PHASE 1: Bug Fix Creation](#phase-1-bug-fix-creation)
6. [Bug Fix Tracking](#bug-fix-tracking)
7. [Current Status](#current-status)
8. [Agent Status (PAUSED - Bug Fix in Progress)](#agent-status-paused---bug-fix-in-progress)
9. [PHASE 2: Bug Fix Implementation](#phase-2-bug-fix-implementation)
10. [Root Cause](#root-cause)
11. [Solution](#solution)
12. [Testing](#testing)
13. [Phase 1: Fix Implementation](#phase-1-fix-implementation)
14. [Phase 2: Testing](#phase-2-testing)
15. [Phase 3: Integration Verification](#phase-3-integration-verification)
16. [Phase 4: Documentation](#phase-4-documentation)
17. [PHASE 3: Resume Previous Work](#phase-3-resume-previous-work)
18. [Priority Handling](#priority-handling)
19. [Completion Criteria](#completion-criteria)
20. [Common Mistakes](#common-mistakes)
21. [Exit Criteria](#exit-criteria)
22. [Summary](#summary)

---
## 🚨 MANDATORY READING PROTOCOL

**BEFORE creating a bug fix, you MUST:**

1. **Use the phase transition prompt** from `prompts_reference_v2.md`
   - Find "Creating Bug Fix" prompt
   - Speak it out loud (acknowledge requirements)

2. **Update README Agent Status** with:
   - Current Phase: BUG_FIX_CREATION
   - Current Guide: stages/s5/s5_bugfix_workflow.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "Get user approval first", "Create notes.txt", "Update epic docs"
   - Next Action: Create bugfix_{priority}_{name} folder

3. **Get user approval** before creating bug fix folder

4. **THEN AND ONLY THEN** proceed with bug fix creation

---

## Prerequisites

**Before starting bug fix workflow:**

- [ ] Bug or missing scope discovered during S5 (implementation) OR reported by user
- [ ] Bug is clearly defined (not a vague issue)
- [ ] Epic is in progress (has active feature work)
- [ ] Read prompts_reference_v2.md "Creating Bug Fix" prompt
- [ ] Working directory: Epic folder root

**If any prerequisite fails:**
- Define bug clearly before proceeding
- If not during epic work, use standard feature workflow instead

---

## Overview

**What is this guide?**
Bug Fix Workflow is a streamlined process for handling bugs discovered during epic implementation, using a simplified workflow (S2 → S5 → S6 → S7) that skips epic-level stages while maintaining full rigor for quality.

**When do you use this guide?**
- Bug discovered during S5 (feature implementation) or reported by user
- Need to fix bug without disrupting epic progress
- Ready to create focused bug fix

**Key Outputs:**
- ✅ bugfix_{priority}_{name} folder created inside epic folder
- ✅ notes.txt created and user-verified
- ✅ Bug fix implemented through simplified workflow (S2 → S5 → S6 → S7)
- ✅ Epic documentation updated for resumability
- ✅ Ready to resume previous work

**Time Estimate:**
Varies by bug complexity (30 minutes to 2 hours typical)

**Exit Condition:**
Bug Fix is complete when the bug is fixed through the full workflow (including all 22 iterations and QC rounds), bug fix folder remains in epic directory, and epic README documents where to resume previous work

---

## 🛑 Critical Rules

```text
1. ⚠️ GET USER APPROVAL FIRST
   - Don't automatically create bug fix
   - Present issue to user
   - Ask: "Should I create bug fix or continue?"
   - User decides priority level

2. ⚠️ CREATE NOTES.TXT (User verifies)
   - Agent writes initial notes.txt
   - User reviews and updates if needed
   - User approval required before proceeding

3. ⚠️ UPDATE EPIC DOCS FOR RESUMABILITY
   - Document current work state before switching
   - Update epic README with bug fix status
   - Add to Bug Fix Tracking table
   - Future agent must know where to resume

4. ⚠️ FOLLOW SIMPLIFIED WORKFLOW
   - Bug fixes: S2 → S5 → S6 → S7
   - SKIP: Stages 1, 3, 4, S8, S9, S10
   - Same rigor as features (22 iterations, QC rounds)
   - No shortcuts

5. ⚠️ PRIORITY DETERMINES INTERRUPTION
   - high: Interrupt immediately
   - medium: Finish current sub-stage first
   - low: Finish current feature first

6. ⚠️ BUG FIX STAYS IN EPIC FOLDER
   - Don't move to done/ until epic completes
   - Easier for epic-level QC
   - All epic work stays together

7. ⚠️ RETURN TO PREVIOUS WORK AFTER COMPLETION
   - Bug fix folder stays in epic directory
   - README Agent Status shows where to resume
   - Continue epic from where it left off
```

---

## PHASE 1: Bug Fix Creation

### Step 1: Discover Issue

**Trigger scenarios:**
- QC round finds critical bug in just-completed feature
- User reports issue with existing feature
- Agent discovers missing scope during implementation
- Integration testing reveals conflict between features

---

### Step 2: Present to User

**Template:**
```markdown
I've discovered an issue that needs addressing:

## Issue: {Brief description}

**Discovered during:** {Stage and feature}

**Problem:**
{Clear description of what's wrong}

**Impact:**
{What doesn't work because of this}

**Recommendation:**
Create bug fix with priority: {high/medium/low}

**Proposed priority reasoning:**
- high: {Blocks current work / Critical functionality broken}
- medium: {Non-blocking but important / Affects user experience}
- low: {Minor issue / Can wait until after current feature}

Should I:
1. Create bug fix now (interrupts current work)
2. Document issue and continue (address later)
3. Other approach

What would you like to do?
```

**Wait for user response**

---

### Step 3: Create Bug Fix Folder

**If user approves:**

1. **Determine folder name:**
   ```text
   bugfix_{priority}_{short_name}/

   Examples:
   - bugfix_high_authentication_error/
   - bugfix_medium_missing_adp_multiplier/
   - bugfix_low_typo_in_logs/
   ```

2. **Create folder in epic directory:**
   ```text
   feature-updates/KAI-{N}-{epic_name}/bugfix_{priority}_{name}/
   ```

3. **Create initial structure:**
   ```text
   bugfix_{priority}_{name}/
   ├── notes.txt        (create now - user verifies)
   ├── spec.md          (create in S2)
   ├── checklist.md     (create in S2)
   ├── implementation_plan.md (create in S5)
   ├── implementation_checklist.md (create in S6)
   └── lessons_learned.md (create in S7 (Testing & Review))
   ```

---

### Step 4: Create notes.txt

**Template:**
```text
BUG FIX: {name}
Priority: {high/medium/low}
Discovered: {date}
Discovered During: {Stage X - feature_name}

----

ISSUE DESCRIPTION:

{Clear description of the bug/issue}

What's wrong:
- {Symptom 1}
- {Symptom 2}
- {Symptom 3}

How discovered:
- {How the issue was found - e.g., "QC Round 2 revealed...", "User reported..."}

Impact:
- {What doesn't work because of this bug}
- {Who is affected}
- {How severe}

----

ROOT CAUSE (if known):

{Analysis of why the bug exists}

Example:
- Missing null check in ConfigManager.get_adp_multiplier()
- When player has no ADP data, method crashes instead of returning default

----

PROPOSED SOLUTION:

{How to fix it}

Example:
- Add null check at top of method
- Return (1.0, 50) for null/missing ADP (neutral multiplier)
- Add unit test for null ADP case

----

VERIFICATION PLAN:

How to verify fix works:
1. {Test scenario 1}
2. {Test scenario 2}
3. {Expected result}

----

USER NOTES:

{User can add notes, clarifications, or corrections here}
```

---

### Step 5: User Verification

**Actions:**
1. Save notes.txt
2. Ask user to review and update notes.txt
3. Wait for user approval

**Template:**
```text
I've created bugfix_{priority}_{name}/notes.txt with the issue description.

Please review and update if needed:
- Is the problem description accurate?
- Is the root cause correct?
- Is the proposed solution appropriate?
- Anything to add or clarify?

Once you've reviewed, let me know and I'll proceed with the bug fix workflow.
```

---

### Step 6: Update Epic Documentation

**Update EPIC_README.md:**

**Add to Bug Fix Tracking table:**
```markdown
### Bug Fix Tracking

| # | Bug Fix Name | Priority | Status | Notes |
|---|--------------|----------|--------|-------|
| 1 | bugfix_high_authentication_error | high | S2 | Discovered during feature_01 QC |
```

**Add to Current Status section:**
```markdown
### Current Status

**Last Updated:** 2025-12-30 18:00

**Active Bug Fixes:**
- bugfix_high_authentication_error (S2 - Deep Dive)
  - Discovered: During feature_01 QC Round 2
  - Priority: high (blocks feature_02 implementation)
  - Currently: Creating spec.md for bug fix

**Paused Work:**
- feature_01_adp_integration: Paused at S7 (Testing & Review) (post-implementation)
  - Resume point: After bug fix complete, verify fix doesn't affect feature_01
  - Agent Status saved: README.md in feature_01/ folder
```

---

### Step 7: Save Current Work State

**Update current feature's README.md:**

```markdown
### Agent Status (PAUSED - Bug Fix in Progress)

**Last Updated:** 2025-12-30 18:00
**Status:** PAUSED for bugfix_high_authentication_error
**Paused At:** S7 (Testing & Review) - QC Round 2 (found bug, creating fix)

**Resume Instructions:**
When bug fix complete:
1. Re-run S7 (Testing & Review) QC Round 2 (verify bug fix didn't affect this feature)
2. If passes: Continue to QC Round 3
3. If fails: Investigate interaction with bug fix

**Context at Pause:**
- QC Round 1: PASSED
- QC Round 2: In progress - found authentication bug that affects this feature
- Bug discovered: ConfigManager.get_adp_multiplier() crashes on null ADP
- This feature calls get_adp_multiplier() - need to verify fix works correctly
```

---

## PHASE 2: Bug Fix Implementation

**Bug fixes follow SIMPLIFIED workflow:**

```text
S2 (Deep Dive) →
S5 (Implementation Planning) →
S6 (Implementation) →
S7 (Testing & Review) (Post-Implementation) →
DONE (return to previous work)
```

**SKIP these stages:**
- ❌ S1 (Epic Planning) - epic already planned
- ❌ S3 (Cross-Feature Sanity Check) - not needed for single bug
- ❌ S4 (Epic Testing Strategy) - not needed for single bug
- ❌ S8.P1 - bug fix doesn't affect other specs
- ❌ S8.P2 (Epic Testing Update) (Epic Testing Plan Update) - handled in S7 (Testing & Review)
- ❌ S9 (Epic Final QC) - bug fix has own QC in S7 (Testing & Review)
- ❌ S10 (Epic Cleanup) - bug stays with epic

---

### S2: Deep Dive (Adapted for Bug Fixes)

**Read:** stages/s2/s2_feature_deep_dive.md

**Adapt for bug fix:**
1. **Create spec.md** (bug fix requirements)
   - What needs to be fixed
   - Root cause analysis
   - Solution approach
   - Verification plan

2. **Create checklist.md** (decisions for bug fix)
   - Usually shorter than feature checklists
   - Focus on fix approach decisions

3. **Create lessons_learned.md** (why bug happened, how to prevent)

4. **Skip:** Cross-feature alignment (not needed for bug)

**Keep spec.md focused:**
```markdown
# Bug Fix: Authentication Error

### Root Cause

ConfigManager.get_adp_multiplier() crashes when player has null ADP value.

Location: league_helper/util/ConfigManager.py:234

```
def get_adp_multiplier(self, adp_value: float) -> Tuple[float, int]:
    # BUG: No null check
    if adp_value < 10:  # Crashes if adp_value is None
        return (1.50, 100)
```markdown

### Solution

Add null check at method start:

```
def get_adp_multiplier(self, adp_value: float) -> Tuple[float, int]:
    # FIX: Handle null/missing ADP
    if adp_value is None:
        self.logger.info("ADP value missing, using neutral multiplier")
        return (1.0, 50)

    if adp_value < 10:
        return (1.50, 100)
```markdown

### Testing

Unit tests:
- test_get_adp_multiplier_with_none()
- test_get_adp_multiplier_with_zero()

Integration test:
- Verify PlayerManager handles None ADP gracefully
```

---

### S5: Implementation Planning

**Read guides in order:**
1. stages/s5/s5_p1_planning_round1.md - Round 1 (iterations 1-7 + 4a)
2. stages/s5/s5_p2_planning_round2.md - Round 2 (iterations 8-13)
3. stages/s5/s5_p3_i1_preparation.md - Round 3 Part 1 (iterations 14-19)
4. stages/s5/s5_p3_i3_gates_part2.md - Round 3 Part 2 (iterations 23, 23a, 25, 24)

**Same rigor as features:**
- Complete ALL 24 verification iterations
- Algorithm Traceability Matrix
- Mock Audit
- Pre-Implementation Spec Audit

**Bug fix TODOs usually shorter:**
```markdown
# Bug Fix TODO: Authentication Error

### Phase 1: Fix Implementation
- [ ] Add null check to ConfigManager.get_adp_multiplier()
- [ ] Add logging for missing ADP case
- [ ] Update method docstring

### Phase 2: Testing
- [ ] Add unit test: test_get_adp_multiplier_with_none()
- [ ] Add unit test: test_get_adp_multiplier_with_zero()
- [ ] Run all ConfigManager tests (verify no regressions)

## Phase 3: Integration Verification
- [ ] Test PlayerManager with None ADP
- [ ] Verify feature_01 still works after fix
- [ ] Run full test suite (100% pass required)

## Phase 4: Documentation
- [ ] Update implementation_checklist.md
```

---

### S6: Implementation

**Read:** stages/s6/s6_execution.md

**Same process as features:**
- Interface Verification Protocol
- Keep spec.md visible
- Phase-by-phase implementation
- Run tests after each step
- Update implementation_checklist.md

---

### S7 (Testing & Review): Post-Implementation

**Read guides in order:**
1. stages/s7/s7_p1_smoke_testing.md - Smoke Testing (3 parts - MANDATORY GATE)
2. stages/s7/s7_p2_qc_rounds.md - QC Round 1, 2, 3 (with restart protocol)
3. stages/s7/s7_p3_final_review.md - PR Review (11 categories) + lessons learned

**Same validation as features:**
- Smoke Testing (3 parts)
- QC Round 1, 2, 3
- PR Review (11 categories)
- QC Restart Protocol if issues found

**Bug fix smoke testing:**
```bash
# Part 1: Import test
python -c "from league_helper.util.ConfigManager import ConfigManager"

# Part 2: Entry point test (if applicable)
python run_league_helper.py --help

# Part 3: E2E test
# Run scenario that triggered bug
# Verify bug no longer occurs
python run_league_helper.py --mode draft
# Check: Players with missing ADP work correctly
```

---

## PHASE 3: Resume Previous Work

### Step 1: Mark Bug Fix Complete

**Update EPIC_README.md:**

```markdown
### Bug Fix Tracking

| # | Bug Fix Name | Priority | Status | Notes |
|---|--------------|----------|--------|-------|
| 1 | bugfix_high_authentication_error | high | COMPLETE | Fixed null ADP handling |

### Current Status

**Completed Bug Fixes:**
- bugfix_high_authentication_error:
  - Completed: 2025-12-30 19:00
  - Solution: Added null check to ConfigManager.get_adp_multiplier()
  - Verification: All tests pass, feature_01 retested successfully

**Resuming Work:**
- feature_01_adp_integration: Resuming S7 (Testing & Review) (post-implementation)
  - Resume from: QC Round 2 (re-run after bug fix)
  - Next action: Complete QC Round 2, then Round 3
```

---

### Step 2: Verify Bug Fix Doesn't Affect Paused Work

**Check:**
- Does bug fix change interfaces paused feature uses?
- Does bug fix affect data structures paused feature depends on?
- Does bug fix require retesting paused feature?

**Example:**
```bash
Bug fix: Added null check to ConfigManager.get_adp_multiplier()

Paused feature: feature_01_adp_integration

Impact check:
- feature_01 calls get_adp_multiplier() → AFFECTED
- Need to re-run feature_01's QC to verify fix didn't break it

Action: Re-run feature_01 S7 (Testing & Review) QC Round 2 before continuing
```

---

### Step 3: Resume from Saved State

**Read paused feature's README.md:**
```markdown
### Agent Status (PAUSED - Bug Fix in Progress)

**Resume Instructions:**
When bug fix complete:
1. Re-run S7 (Testing & Review) QC Round 2 (verify bug fix didn't affect this feature)
2. If passes: Continue to QC Round 3
3. If fails: Investigate interaction with bug fix
```

**Follow resume instructions explicitly**

---

### Step 4: Update README Agent Status

```markdown
**Current Phase:** POST_IMPLEMENTATION_QC_ROUNDS (Resumed)
**Current Guide:** stages/s7/s7_p2_qc_rounds.md
**Guide Last Read:** 2025-12-30 19:15
**Resumed After:** bugfix_high_authentication_error completion
**Next Action:** Re-run QC Round 2 to verify bug fix compatibility
```

---

## Priority Handling

### High Priority

**When:** Bug blocks current work or breaks critical functionality

**Action:** Interrupt immediately

**Example:**
```text
Currently: feature_01 S6 (implementation)
Bug discovered: ConfigManager crashes (blocks feature_01)
Priority: high

Action:
1. Save feature_01 state (update README)
2. Create bug fix immediately
3. Complete bug fix (S2 → S7)
4. Resume feature_01 S6
```

---

### Medium Priority

**When:** Bug doesn't block but affects user experience

**Action:** Finish current sub-stage, then switch

**Example:**
```text
Currently: feature_02 S6 Phase 2 (of 4 phases)
Bug discovered: Log messages unclear
Priority: medium

Action:
1. Complete Phase 2
2. Save feature_02 state (at end of Phase 2)
3. Create and fix bug
4. Resume feature_02 Phase 3
```

---

### Low Priority

**When:** Minor issue that can wait

**Action:** Finish current feature, then switch

**Example:**
```text
Currently: feature_03 S7 (Testing & Review) (QC Round 2)
Bug discovered: Typo in output message
Priority: low

Action:
1. Complete feature_03 through S8.P2 (Epic Testing Update)
2. Then create and fix bug
3. Continue to next feature
```

---

## Completion Criteria

**Bug fix is complete when:**

- [x] notes.txt created and user-verified
- [x] spec.md created (root cause, solution)
- [x] checklist.md created
- [x] S5 complete (22 iterations, implementation_plan.md)
- [x] S6 complete (implementation, tests pass)
- [x] S7 (Testing & Review) complete (smoke tests, QC rounds, PR review)
- [x] lessons_learned.md updated
- [x] Epic README updated (bug fix marked complete)
- [x] Previous work verified compatible with fix
- [x] Ready to resume previous work

---

## Common Mistakes

### Anti-Pattern 1: Skipping User Approval

**Mistake:** Agent discovers bug and immediately creates bug fix folder

**Why wrong:** User should decide priority and whether to fix now

**Correct:** Present issue, get approval, then create folder

---

### Anti-Pattern 2: Shortcuts in Bug Fix QC

**Mistake:** "It's just a small bug, I'll skip QC rounds"

**Why wrong:** Small bugs can have big impacts. Same rigor required.

**Correct:** Full S7 (Testing & Review) validation (smoke tests + Validation Loop (3 consecutive clean rounds) + PR review)

---

### Anti-Pattern 3: Not Updating Epic Docs

**Mistake:** Create bug fix but don't update EPIC_README or feature README

**Why wrong:** Future agent won't know bug fix exists or where to resume

**Correct:** Update both epic README and paused feature's README

---

### Anti-Pattern 4: Forgetting to Resume

**Mistake:** Complete bug fix, then start new work without resuming paused feature

**Why wrong:** Paused feature left incomplete

**Correct:** Resume paused work, verify compatibility, complete paused feature

---

## Exit Criteria

**Bug fix workflow is complete when ALL of these are true:**

- [ ] User approved bug fix creation (priority and timing decided)
- [ ] bugfix_{priority}_{name}/ folder created with complete structure
- [ ] notes.txt created and user-verified
- [ ] Bug fix workflow followed (S2 → S5 → S6 → S7 with full rigor)
- [ ] All 22 iterations completed in S5 (no shortcuts)
- [ ] QC rounds passed (S7)
- [ ] Bug fix tested and verified
- [ ] Epic documentation updated for resumability
- [ ] Paused work resumed cleanly with compatibility verification
- [ ] Bug fix remains in epic folder (not moved to done/)

**If any criterion unchecked:** Complete missing items before considering bug fix done

---

## Summary

**Bug fix workflow ensures bugs are fixed properly without disrupting epic progress:**

1. **Get approval** - User decides priority and timing
2. **Document thoroughly** - notes.txt user-verified
3. **Follow simplified workflow** - S2 → S5 → S6 → S7
4. **Same rigor** - 22 iterations, QC rounds, no shortcuts
5. **Resume cleanly** - Return to paused work, verify compatibility

**Critical:**
- Bug fixes stay in epic folder (don't move to done/)
- Same validation rigor as features
- Priority determines interruption timing
- Epic docs updated for resumability

---

*End of stages/s5/s5_bugfix_workflow.md*
