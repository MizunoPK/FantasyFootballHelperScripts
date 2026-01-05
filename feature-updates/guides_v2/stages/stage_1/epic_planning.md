# STAGE 1: Epic Planning Guide

🚨 **MANDATORY READING PROTOCOL**

**Before starting this stage:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update epic EPIC_README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check epic EPIC_README.md Agent Status for current phase
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**What is this stage?**
Epic Planning is the first stage where you create the git branch, analyze the user's epic request, break it down into features, validate your understanding through an epic ticket, and create the folder structure for the entire epic.

**When do you use this guide?**
- User has created `{epic_name}.txt` with their epic request
- Starting a new epic from scratch
- Need to plan multi-feature work

**Key Outputs:**
- ✅ Git branch created for epic work
- ✅ Epic ticket created and user-validated (confirms understanding)
- ✅ Epic folder structure created (EPIC_README, epic_smoke_test_plan, feature folders)
- ✅ Initial test plan documented
- ✅ Ready to start Stage 2 (feature deep dives)

**Time Estimate:**
45-75 minutes (includes epic ticket validation)

**Exit Condition:**
Stage 1 is complete when you have a validated epic ticket, complete folder structure, and user has confirmed the feature breakdown

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ CREATE GIT BRANCH BEFORE ANY CHANGES (Step 1.0)
   - Verify on main, pull latest
   - Assign KAI number from EPIC_TRACKER.md
   - Create branch: {work_type}/KAI-{number}
   - Update EPIC_TRACKER.md and commit immediately

2. ⚠️ USER MUST APPROVE feature breakdown before creating epic ticket
   - Agent proposes breakdown
   - User confirms/modifies
   - Do NOT proceed without approval

3. ⚠️ CREATE EPIC TICKET and get user validation (Steps 3.6-3.7)
   - Epic ticket validates agent understanding of outcomes
   - User must approve epic ticket before folder creation
   - Epic ticket becomes immutable reference (like epic notes)

4. ⚠️ Create GUIDE_ANCHOR.md in epic folder (resumption instructions)

5. ⚠️ epic_smoke_test_plan.md is PLACEHOLDER (will update in Stages 4, 5e)
   - Initial plan based on assumptions
   - Mark clearly as "INITIAL - WILL UPDATE"

6. ⚠️ Update EPIC_README.md Agent Status after EACH major step

7. ⚠️ Feature numbering: feature_01_{name}, feature_02_{name}, etc.
   - Consistent zero-padded numbering
   - Descriptive names (not generic)

8. ⚠️ Create research/ folder in epic root (shared across all features)

9. ⚠️ Epic planning does NOT include deep dives
   - Stage 1: Create structure, propose features
   - Stage 2: Deep dive per feature (separate stage)

10. ⚠️ If unsure about feature breakdown, propose FEWER features
    - Can add features during Stage 2 (discovery)
    - Harder to merge features later

11. ⚠️ Every feature MUST have clear purpose (1-2 sentences)
    - Avoid "miscellaneous" or "utilities" features
    - Each feature delivers distinct value

12. ⚠️ Mark completion in EPIC_README.md before transitioning to Stage 2
```

---

## Critical Decisions Summary

**Stage 1 has 4 major decision points. Know these before starting:**

### Decision Point 1: Determine Work Type (Step 1.0d)
**Question:** Is this an epic, feat, or fix?
- **epic:** Work with multiple features (most epics)
- **feat:** Work with single feature only
- **fix:** Bug fix work
- **Impact:** Determines branch name format and EPIC_TRACKER classification

### Decision Point 2: Feature Breakdown Approval (Phase 3)
**Question:** Does the user approve the proposed feature list?
- **If NO:** User provides feedback, agent revises breakdown
- **If YES:** Proceed to create epic ticket (Step 3.6)
- **Impact:** Defines entire epic structure - cannot easily change after folders created

### Decision Point 3: Epic Ticket Validation (Steps 3.6-3.7)
**Question:** Does the epic ticket accurately reflect user's desired outcomes?
- **If NO:** User corrects misunderstandings, agent updates epic ticket
- **If YES:** Proceed to folder creation (Phase 4)
- **Impact:** Epic ticket becomes immutable reference - validates agent understanding

### Decision Point 4: Feature Folder Creation (Step 4.2)
**Question:** Create correct number of feature folders matching approved breakdown?
- **Verify:** Feature count matches approved list
- **Verify:** Feature names are descriptive (not generic)
- **Impact:** Epic structure is set - adding features later requires returning to Stage 1

**Note:** Each decision point has clear criteria. Read the detailed section before making decision.

---

## Prerequisites Checklist

**Verify BEFORE starting Stage 1:**

□ User has created `feature-updates/{epic_name}.txt` with epic request notes
□ Epic request file contains sufficient detail (problem description, goals, constraints)
□ No existing epic folder with same name (check `feature-updates/` directory)
□ Git working directory is clean (no uncommitted changes that could conflict)

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with Stage 1
- Ask user to resolve prerequisite issue
- Document blocker in conversation

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    STAGE 1 WORKFLOW                          │
└──────────────────────────────────────────────────────────────┘

Phase 1: Initial Setup
   ├─ Create git branch for epic (Step 1.0 - BEFORE any changes)
   │  ├─ Verify on main, pull latest
   │  ├─ Assign KAI number from EPIC_TRACKER.md
   │  ├─ Create branch: {work_type}/KAI-{number}
   │  └─ Update EPIC_TRACKER.md and commit
   ├─ Create epic folder
   ├─ Move {epic_name}.txt into epic folder
   └─ Create EPIC_README.md (with Agent Status)

Phase 2: Epic Analysis
   ├─ Read epic request thoroughly
   ├─ Identify goals, constraints, requirements
   └─ Conduct broad codebase reconnaissance

Phase 3: Feature Breakdown Proposal
   ├─ Identify major components/subsystems
   ├─ Propose feature list with justification
   ├─ Present to user for approval
   ├─ WAIT for user confirmation/modifications
   ├─ Create epic ticket (outcome validation)
   └─ WAIT for user validation of epic ticket

Phase 4: Epic Structure Creation
   ├─ Create feature folders (per approved breakdown)
   ├─ Create epic_smoke_test_plan.md (initial)
   ├─ Create epic_lessons_learned.md
   ├─ Create research/ folder
   ├─ Create GUIDE_ANCHOR.md
   └─ Update EPIC_README.md with feature tracking table

Phase 5: Transition to Stage 2
   ├─ Mark Stage 1 complete in EPIC_README.md
   ├─ Update Agent Status (next: Stage 2)
   └─ Announce transition to user
```

---

## Phase 1: Initial Setup

### Step 1.0: Create Git Branch for Epic

**CRITICAL:** Create branch BEFORE making any changes to codebase.

**Why branch first:**
- Keeps main branch clean and stable
- Allows parallel work on multiple epics
- Enables easy rollback if needed
- Follows standard git workflow practices

**Actions:**

**1.0a. Verify you're on main branch:**

```bash
git checkout main
```

**Expected output:**
```
Already on 'main'
Your branch is up to date with 'origin/main'.
```

**1.0b. Pull latest changes from origin:**

```bash
git pull origin main
```

**Expected output:**
```
From github.com:user/repo
 * branch            main       -> FETCH_HEAD
Already up to date.
```

**If there are conflicts:** Resolve them before proceeding.

**1.0c. Assign KAI number:**

Check `feature-updates/EPIC_TRACKER.md` for next available KAI number.

**Example:** If EPIC_TRACKER.md shows "Next Available Number: KAI-1", use KAI-1.

**1.0d. Determine work type:**

- `epic` - Work includes multiple features (most common)
- `feat` - Work is a single feature only
- `fix` - Work is already classified as a bug fix

**For most epics:** Use `epic`

**1.0e. Create and checkout branch:**

```bash
git checkout -b {work_type}/KAI-{number}
```

**Examples:**
- `git checkout -b epic/KAI-1` (multi-feature epic)
- `git checkout -b feat/KAI-2` (single feature)
- `git checkout -b fix/KAI-3` (bug fix)

**Verify branch created:**

```bash
git branch
```

**Expected output:**
```
* epic/KAI-1
  main
```

(The `*` indicates your current branch)

**1.0f. Update EPIC_TRACKER.md:**

Add epic to "Active Epics" table:

```markdown
| KAI # | Epic Name | Type | Branch | Status | Date Started |
|-------|-----------|------|--------|--------|--------------|
| 1 | {epic_name} | epic | epic/KAI-1 | In Progress | 2025-12-31 |
```

**Increment "Next Available Number":**
```markdown
### Next Available Number: KAI-2
```

**Commit EPIC_TRACKER.md update:**

```bash
git add feature-updates/EPIC_TRACKER.md
git commit -m "feat/KAI-1: Initialize epic tracking for {epic_name}"
```

**Why commit EPIC_TRACKER.md immediately:**
- Documents epic start in git history
- Prevents number conflicts if multiple agents work simultaneously
- Establishes branch with first commit

---

### Step 1.1: Create Epic Folder

```bash
mkdir -p feature-updates/KAI-{N}-{epic_name}/
```

**Example:** `mkdir -p feature-updates/KAI-1-improve_draft_helper/`

**Folder Naming Rules:**
- Format: `KAI-{N}-{epic_name}/` (includes KAI number assigned in step 1.0c)
- Use snake_case for epic_name (not spaces or hyphens)
- Descriptive name matching epic request file
- Example: `KAI-1-improve_draft_helper`, not `improve-draft-helper` or `KAI-1-ImproveD raftHelper`

**Why include KAI number in folder name:**
- Ensures unique folder names (prevents conflicts)
- Matches branch naming convention (`epic/KAI-{N}`)
- Enables quick identification of epic by number
- Maintains consistency across git branches and file system

### Step 1.2: Move Epic Request File

```bash
mv feature-updates/{epic_name}.txt feature-updates/KAI-{N}-{epic_name}/{epic_name}_notes.txt
```

**Example:** `mv feature-updates/improve_draft_helper.txt feature-updates/KAI-1-improve_draft_helper/improve_draft_helper_notes.txt`

**Why rename to `_notes.txt`:**
- Distinguishes from feature spec files
- Signals this is original scratchwork (reference only)
- Consistent naming across all epics

**Note:** Original request file (`{epic_name}.txt`) does NOT include KAI number, but the epic folder DOES

### Step 1.3: Create EPIC_README.md

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "Epic README Template"

**Initial Agent Status:**
```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** EPIC_PLANNING
**Current Step:** Phase 1 - Initial Setup Complete
**Current Guide:** stages/stage_1/epic_planning.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- User must approve feature breakdown before creating folders
- epic_smoke_test_plan.md is placeholder (will update in Stages 4, 5e)
- Update Agent Status after each major step

**Progress:** 1/5 phases complete (Initial Setup)
**Next Action:** Phase 2 - Epic Analysis
**Blockers:** None
```

### Step 1.4: Update Agent Status

After completing Phase 1:
- Update "Last Updated" timestamp
- Update "Progress" to "1/5 phases complete"
- Update "Next Action" to "Phase 2 - Epic Analysis"

---

## Phase 2: Epic Analysis

**Goal:** Understand epic request and identify major components

**DO NOT:**
- ❌ Jump to implementation details
- ❌ Deep dive into specific features (that's Stage 2)
- ❌ Write code or create detailed specs

**DO:**
- ✅ Read epic request thoroughly (multiple times)
- ✅ Identify high-level goals and constraints
- ✅ Conduct broad codebase reconnaissance
- ✅ Understand existing patterns to leverage

### Step 2.1: Read Epic Request Thoroughly

Read `{epic_name}_notes.txt` and answer:

1. **What problem is this epic solving?**
   - User pain point or missing capability
   - Example: "Users can't track player performance trends"

2. **What are the explicit goals?**
   - List measurable outcomes
   - Example: "Generate weekly performance reports for all players"

3. **What constraints are mentioned?**
   - Technical, time, resource limitations
   - Example: "Must use existing CSV data format"

4. **What's explicitly OUT of scope?**
   - Features user said "not now" or "future work"
   - Example: "Not including historical data beyond current season"

### Step 2.2: Identify Major Components Affected

**Quick searches to find:**

```bash
# Example searches (adjust based on epic)
grep -r "PlayerManager" --include="*.py"
grep -r "FantasyTeam" --include="*.py"
grep -r "class.*Manager" --include="*.py"
```

**Ask yourself:**
- Which managers/classes will change?
- Which modules/subsystems are involved?
- Are there similar existing features to reference?

**Document findings:**
```markdown
**Components Likely Affected:**
- PlayerManager (league_helper/util/PlayerManager.py)
- DraftHelper (league_helper/add_to_roster_mode/)
- ConfigManager (league_helper/util/ConfigManager.py)

**Similar Existing Features:**
- Trade simulator mode (similar workflow pattern)
- Starter helper mode (similar data requirements)
```

### Step 2.3: Estimate Rough Scope

**Tag the epic:**
- **SMALL:** 1-2 features, straightforward implementation
- **MEDIUM:** 3-5 features, some complexity, cross-module changes
- **LARGE:** 6+ features, high complexity, multiple subsystems

**Add to EPIC_README.md:**
```markdown
## Initial Scope Assessment

**Size:** MEDIUM (estimated 4 features)
**Complexity:** MODERATE
**Risk Level:** MEDIUM
**Estimated Components:** 5-7 classes/modules affected
```

### Step 2.4: Update Agent Status

After Phase 2:
- Progress: "2/5 phases complete (Epic Analysis)"
- Next Action: "Phase 3 - Feature Breakdown Proposal"

---

## Phase 3: Feature Breakdown Proposal

**Goal:** Propose how to break epic into features (user must approve)

**CRITICAL:** This is a PROPOSAL, not a decision. User must confirm.

### Step 3.1: Identify Feature Breakdown Criteria

Use these criteria to propose features:

**Each feature should:**
1. **Deliver distinct value** (user can describe benefit in 1 sentence)
2. **Be independently testable** (can verify without other features)
3. **Have clear boundaries** (knows what's in vs out of scope)
4. **Be reasonably sized** (20-50 implementation items estimate)
5. **Have defined dependencies** (knows what it needs from other features)

**Examples:**

**GOOD Breakdown:**
```
Epic: Improve Draft Helper
├─ Feature 1: ADP Integration (load ADP data, normalize values)
├─ Feature 2: Injury Risk Assessment (evaluate injury history, calculate penalty)
├─ Feature 3: Schedule Strength Analysis (future opponent analysis)
└─ Feature 4: Recommendation Engine Updates (integrate new data sources)
```

**BAD Breakdown:**
```
Epic: Improve Draft Helper
├─ Feature 1: Data stuff (too vague)
├─ Feature 2: Calculations (too vague)
├─ Feature 3: UI changes (mixing unrelated concerns)
└─ Feature 4: Miscellaneous improvements (no clear purpose)
```

### Step 3.2: Draft Feature Breakdown

For each proposed feature, document:

```markdown
### Feature {N}: {Descriptive Name}

**Purpose:** {1-2 sentence description of what this feature does}

**Scope:**
- {Key capability 1}
- {Key capability 2}
- {Key capability 3}

**Dependencies:**
- **Depends on:** {List other features this needs, or "None"}
- **Blocks:** {List features that need this, or "Unknown yet"}

**Rough Estimate:**
- Implementation items: ~{X} (rough guess)
- Risk: LOW / MEDIUM / HIGH
- Priority: LOW / MEDIUM / HIGH

**Why separate feature:**
- {Reason it's not part of another feature}
```

### Step 3.3: Present Breakdown to User

**Presentation Format:**

```markdown
I've analyzed the epic request and propose breaking this into {N} features:

## Proposed Feature Breakdown

### Feature 1: {Name}
**Purpose:** {description}
**Scope:** {bullet list}
**Dependencies:** {what it needs}
**Estimate:** ~{X} items, {RISK} risk

### Feature 2: {Name}
...

## Rationale

**Why {N} features?**
- {Reason 1 - e.g., "Each addresses distinct subsystem"}
- {Reason 2 - e.g., "Allows parallel testing"}
- {Reason 3 - e.g., "Clear dependency chain"}

**Alternative considered:** {Fewer/more features}
- Rejected because: {reason}

## Recommended Implementation Order

1. Feature {N} (foundation - no dependencies)
2. Feature {N} (depends on Feature 1)
3. Feature {N} (depends on Features 1, 2)
...

**Please review and let me know:**
- Are these the right feature boundaries?
- Should any features be combined or split?
- Are the dependencies correct?
- Should we add or remove any features?
```

### Step 3.4: WAIT for User Approval

⚠️ **STOP HERE - Do NOT proceed without user confirmation**

**DO NOT:**
- ❌ Create feature folders yet
- ❌ Assume user agrees
- ❌ Start Stage 2 deep dives

**DO:**
- ✅ Wait for user response
- ✅ Update EPIC_README.md Agent Status: "Blockers: Waiting for user approval of feature breakdown"
- ✅ Be ready to modify proposal based on user feedback

### Step 3.5: Incorporate User Feedback

**If user requests changes:**
1. Revise feature breakdown based on feedback
2. Update proposal document
3. Present revised breakdown
4. Wait for approval again

**If user approves:**
1. Document approval in EPIC_README.md
2. Proceed to Step 3.6 (Epic Ticket Creation)

---

### Step 3.6: Create Epic Ticket (Outcome Validation)

**Purpose:** Validate agent understands epic outcomes and acceptance criteria BEFORE creating folder structure

**Why this matters:** Catches epic-level misinterpretation early, preventing 40+ hours of work in wrong direction

---

**Template:**

```markdown
# Epic Ticket: [Epic Name]

## Description
[2-3 sentences describing what this epic achieves and why it matters]

## Acceptance Criteria (Epic-level)
- [ ] [Testable outcome 1 - applies to ENTIRE epic]
- [ ] [Testable outcome 2]
- [ ] [Testable outcome 3]
- [ ] [Testable outcome 4]

## Success Indicators
- [Measurable metric 1]
- [Measurable metric 2]
- [Measurable metric 3]

## Failure Patterns (How we'd know epic failed)
❌ [Symptom of failure 1]
❌ [Symptom of failure 2]
❌ [Symptom of failure 3]
```

---

**Guidelines for writing epic ticket:**

**Description:**
- Focus on WHAT is being achieved, not HOW
- Explain why this epic provides value
- Keep to 2-3 sentences maximum

**Acceptance Criteria:**
- Must be testable/verifiable outcomes
- Apply to entire epic (not individual features)
- Use "All X" language when patterns apply broadly (e.g., "All 18 weeks", "All 6 positions")
- Avoid implementation details ("Create class X", "Use method Y")
- Focus on capabilities ("System can...", "Users can...", "Data shows...")

**Success Indicators:**
- Must be measurable/quantifiable
- Examples: "Zero percentage <1%", "All tests pass", "MAE calculation completes"
- Include both positive indicators (what should happen) and thresholds

**Failure Patterns:**
- Describe specific symptoms that would indicate epic failed
- Use patterns from similar past bugs if applicable
- Be explicit about edge cases (e.g., ">90% zeros", "Only week 17-18 work")
- Think: "What would I see in the output if this epic was broken?"

---

**Example - Feature 02 Epic Ticket:**

```markdown
# Epic Ticket: Integrate JSON Player Data into Simulations

## Description
Replace CSV-based player data loading with JSON format for both win rate and accuracy simulations. The new JSON files contain weekly arrays instead of individual columns, enabling more efficient data organization and week-based queries across all 18 NFL regular season weeks.

## Acceptance Criteria
- [ ] Both simulation types (win rate & accuracy) load player data from JSON files
- [ ] All 18 weeks of data are accessible and used correctly for both simulations
- [ ] Actual points for all players across all 18 weeks contain realistic non-zero values
- [ ] Projected points for all players across all 18 weeks contain realistic non-zero values
- [ ] Simulations produce equivalent or better results compared to CSV version
- [ ] No regression in existing simulation functionality
- [ ] All 2,200+ unit tests continue to pass

## Success Indicators
- Actual points have <1% zero values across all weeks/players
- Projected points have <1% zero values across all weeks/players
- Mean absolute error (MAE) calculations complete successfully for all 18 weeks
- Win rate simulations complete 10,000 iterations without errors
- Standard deviation > 0 for both actual and projected points (values have variance)

## Failure Patterns
❌ >90% of actual_points are 0.0 (data loading issue)
❌ Only week 17-18 work while other weeks have zeros (week offset bug)
❌ Calculations return NaN or skip all players (consumption code not updated)
❌ "attribute not found" errors during execution (old API still used)
❌ Mean or standard deviation = 0 (all same value - calculation error)
❌ Only 1-2 players have non-zero values out of 2500 total
```

**Why this would have caught Feature 02 bug:**
- "All 18 weeks" makes clear it's not just week 17-18
- Failure pattern explicitly describes the ">90% zeros" bug that happened
- Success indicators would have failed (99.8% zeros >> 1% threshold)

---

**Process:**

1. **Draft epic ticket** using template above
2. **Save to:** `feature-updates/{epic_name}/EPIC_TICKET.md`
3. **Present to user** for validation
4. **Proceed to Step 3.7** for user sign-off

---

### Step 3.7: User Validation of Epic Ticket

⚠️ **STOP HERE - Do NOT proceed without user validation**

**Present epic ticket to user:**

```markdown
## Epic Ticket Validation Checkpoint

I've created an epic ticket to validate my understanding of the epic's goals and acceptance criteria.

**Location:** `feature-updates/{epic_name}/EPIC_TICKET.md`

**Please review:**
1. **Description** - Does this accurately describe what we're trying to achieve?
2. **Acceptance Criteria** - Are these the right outcomes to measure success?
3. **Success Indicators** - Are these measurable and realistic?
4. **Failure Patterns** - Do these describe what "broken" would look like?

**Questions:**
- Does the epic ticket match your understanding of the epic request?
- Are there any missing acceptance criteria I should add?
- Are there any failure patterns I should include?
- Should I adjust any success indicator thresholds?

**Once you approve the epic ticket, I'll proceed to create the folder structure.**
```

**If user requests changes:**
1. Update EPIC_TICKET.md based on feedback
2. Present updated version
3. Wait for approval again

**If user approves:**
1. Document validation in EPIC_README.md:
   ```markdown
   - [x] Epic ticket created and user-validated (Step 3.7)
   ```
2. Epic ticket is now **immutable reference** (like epic notes)
3. Proceed to Phase 4

**Critical:** Epic ticket becomes source of truth for outcomes. During Iteration 25 (Stage 5ac), spec.md will be validated against both epic notes AND epic ticket.

---

## Phase 4: Epic Structure Creation

**Prerequisites:**
- User has approved feature breakdown
- User has validated epic ticket

### Step 4.1: Create Feature Folders

For EACH feature in approved breakdown:

```bash
mkdir -p feature-updates/KAI-{N}-{epic_name}/feature_{N}_{descriptive_name}/
```

**Example:** `mkdir -p feature-updates/KAI-1-improve_draft_helper/feature_01_adp_integration/`

**Naming Convention:**
- `feature_01_adp_integration/` (zero-padded numbers)
- `feature_02_injury_assessment/`
- `feature_03_schedule_analysis/`

**For each feature folder, create:**

```bash
cd feature-updates/KAI-{N}-{epic_name}/feature_{N}_{name}/

# Create initial files
touch README.md
touch spec.md
touch checklist.md
touch lessons_learned.md
```

**Example:** `cd feature-updates/KAI-1-improve_draft_helper/feature_01_adp_integration/`

**Populate Feature README.md:**

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "Feature README Template"

**Key sections:**
- Feature Context (part of epic, feature number, purpose)
- Agent Status (PLANNING phase, not started yet)
- Files in This Feature (list of files)
- Feature Completion Checklist (all stages unchecked)

**Populate Initial spec.md:**

```markdown
# Feature {N}: {Descriptive Name}

## Objective

{What this feature accomplishes - copy from Phase 3 proposal}

## Scope

{What's included in THIS feature - copy from Phase 3 proposal}

## Dependencies

**Prerequisites:** {Features that must complete first, or "None"}
**Blocks:** {Features that depend on this one, or "Unknown yet"}

## Initial Estimates

- Implementation items: ~{X}
- Risk level: LOW/MEDIUM/HIGH
- Priority: LOW/MEDIUM/HIGH

## Files Likely Affected

{Based on Phase 2 analysis - rough list, will refine in Stage 2}

---

**Status:** Initial spec created during Stage 1 (Epic Planning)
**Next:** Stage 2 (Feature Deep Dive) will flesh out this spec
```

**Create empty checklist.md:**

```markdown
# Feature {N}: {Name} - Planning Checklist

**Status:** Not started (will populate during Stage 2 deep dive)

**Purpose:** Track open questions and decisions needed for this feature

---

{Will be populated during Stage 2}
```

**Create initial lessons_learned.md:**

```markdown
# Feature {N}: {Name} - Lessons Learned

**Purpose:** Document issues encountered and solutions for this feature

---

## Planning Phase Lessons

{Will be populated during Stage 2 deep dive}

## Implementation Phase Lessons

{Will be populated during Stage 5b implementation}

## Post-Implementation Lessons

{Will be populated during Stage 5c QC}
```

### Step 4.2: Create epic_smoke_test_plan.md

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "Epic Smoke Test Plan Template"

**IMPORTANT:** Mark this as INITIAL VERSION

```markdown
# Epic Smoke Test Plan: {epic_name}

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: INITIAL (Stage 1)**
- Created: {date}
- Based on: Assumptions from epic request (NO implementation knowledge yet)
- Quality: PLACEHOLDER - Will be updated in Stage 4 (after deep dives) and Stage 5e (after each feature)

**Next Updates:**
- Stage 4: Major update based on feature specs and alignment findings
- Stage 5e: Incremental updates after each feature implementation

---

## Epic Success Criteria (INITIAL - WILL REFINE)

**The epic is successful if:**

1. {High-level criterion 1 based on epic request}
2. {High-level criterion 2}
3. {High-level criterion 3}

{Note: These are assumptions. Stage 4 will define specific, measurable criteria.}

---

## Specific Commands/Scenarios (PLACEHOLDER)

**⚠️ These are ROUGH guesses based on epic request. Stage 4 will define actual commands.**

### Test 1: {Test Name}
```bash
# Command TBD after Stage 2 deep dives
```
**Expected result:** TBD
**Failure indicates:** TBD

---

## High-Level Test Categories (INITIAL)

**These categories will be fleshed out in Stage 4 with specific scenarios:**

### Category 1: Cross-Feature Integration
**What to test:** {General idea of integration points}
**Specific scenarios:** TBD in Stage 4

### Category 2: Error Handling
**What to test:** {General error paths}
**Specific scenarios:** TBD in Stage 4

---

## Update Log

| Date | Stage | What Changed | Why |
|------|-------|--------------|-----|
| {date} | Stage 1 | Initial plan created | Epic planning - assumptions only |

**Current version is informed by:**
- Stage 1: Initial assumptions from epic request (THIS VERSION)
- Stage 4: TBD (will update after deep dives)
- Stage 5e updates: TBD (will update after each feature)
```

### Step 4.3: Create epic_lessons_learned.md

```markdown
# Epic: {epic_name} - Lessons Learned

**Purpose:** Document cross-feature patterns and systemic insights from this epic

---

## Planning Phase Lessons (Stages 1-4)

{Will be populated during Stages 1-4}

## Implementation Phase Lessons (Stage 5)

{Will be populated during Stage 5 as features are implemented}

## QC Phase Lessons (Stage 6)

{Will be populated during Stage 6 epic final QC}

## Guide Improvements Identified

{Track guide gaps/improvements discovered during this epic}

| Guide File | Issue | Proposed Fix | Status |
|------------|-------|--------------|--------|
| {guide} | {what was missing/unclear} | {how to fix} | Pending/Done |
```

### Step 4.4: Create research/ Folder

```bash
mkdir -p feature-updates/KAI-{N}-{epic_name}/research/
```

**Example:** `mkdir -p feature-updates/KAI-1-improve_draft_helper/research/`

**Create research/README.md:**

```markdown
# Research and Analysis Documents

This folder contains all research, analysis, and verification reports for the epic.

**Purpose:**
- Keeps epic root folder clean (only EPIC_README, test plan, lessons learned)
- Centralizes reference material shared across features
- Clear separation: feature specs = implementation guidance, research = context

**File Naming:**
- `{TOPIC}_ANALYSIS.md` - Detailed analysis of specific topic
- `VERIFICATION_REPORT_{DATE}.md` - Verification findings
- `RESEARCH_FINDINGS_{DATE}.md` - General research results
- `{FEATURE_NAME}_DISCOVERY.md` - Discoveries from feature deep dive

**All research documents go here from the start.**
```

### Step 4.5: Create GUIDE_ANCHOR.md

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "GUIDE_ANCHOR Template"

**Critical sections:**
- Instructions for resuming after session compaction
- Current stage identification
- Active guide name
- Workflow reference diagram

**This file ensures agents can resume correctly after context window limits.**

### Step 4.6: Update EPIC_README.md

Add **Feature Tracking** table:

```markdown
## Feature Tracking

| # | Feature Name | Stage 2 Complete | Stage 5e Complete | Notes |
|---|--------------|------------------|-------------------|-------|
| 1 | feature_01_{name} | [ ] | [ ] | Not started |
| 2 | feature_02_{name} | [ ] | [ ] | Not started |
| 3 | feature_03_{name} | [ ] | [ ] | Not started |

**Stage 2 Complete:** Spec fleshed out from deep dive
**Stage 5e Complete:** Feature implementation fully complete
```

Add **Epic Completion Checklist:**

```markdown
## Epic Completion Checklist

**Stage 1 - Epic Planning:**
- [x] Epic folder created
- [x] All feature folders created
- [x] Initial epic_smoke_test_plan.md created
- [x] EPIC_README.md created
- [x] GUIDE_ANCHOR.md created
- [x] research/ folder created

**Stage 2 - Feature Deep Dives:**
- [ ] ALL features have spec.md complete
- [ ] ALL features have checklist.md resolved

**Stage 3 - Cross-Feature Sanity Check:**
- [ ] All specs compared systematically
- [ ] Conflicts resolved
- [ ] User sign-off obtained

**Stage 4 - Epic Testing Strategy:**
- [ ] epic_smoke_test_plan.md updated
- [ ] Integration points identified
- [ ] Epic success criteria defined

**Stage 5 - Feature Implementation:**
- [ ] Feature 1: 5a→5b→5c→5d→5e complete
- [ ] Feature 2: 5a→5b→5c→5d→5e complete
- [ ] ... (all features)

**Stage 6 - Epic Final QC:**
- [ ] Epic smoke testing passed
- [ ] Epic QC rounds passed
- [ ] Epic PR review passed
- [ ] End-to-end validation passed

**Stage 7 - Epic Cleanup:**
- [ ] Final commits made
- [ ] Epic moved to done/ folder
```

### Step 4.7: Update Agent Status

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** EPIC_PLANNING
**Current Step:** Phase 4 - Epic Structure Creation Complete
**Current Guide:** stages/stage_1/epic_planning.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- User must approve feature breakdown before creating folders
- epic_smoke_test_plan.md is placeholder (will update in Stages 4, 5e)
- Update Agent Status after each major step

**Progress:** 4/5 phases complete (Epic Structure Created)
**Next Action:** Phase 5 - Transition to Stage 2
**Blockers:** None

**Features Created:**
- feature_01_{name}
- feature_02_{name}
- feature_03_{name}
```

---

## Phase 5: Transition to Stage 2

### Step 5.1: Mark Stage 1 Complete

Update EPIC_README.md Epic Completion Checklist:

```markdown
**Stage 1 - Epic Planning:**
- [x] Epic folder created
- [x] All feature folders created
- [x] Initial epic_smoke_test_plan.md created
- [x] EPIC_README.md created
- [x] GUIDE_ANCHOR.md created
- [x] research/ folder created
```

### Step 5.2: Update Agent Status for Stage 2

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** DEEP_DIVE
**Current Step:** Ready to begin Stage 2a (Research Phase) for Feature 1
**Current Guide:** stages/stage_2/phase_0_research.md
**Guide Last Read:** NOT YET (will read when starting Stage 2a)
**Critical Rules from Guide:** (Will populate after reading Stage 2a guide)

**Progress:** Stage 1 complete, ready for Stage 2a
**Next Action:** Read stages/stage_2/phase_0_research.md and begin research phase for feature_01_{name}
**Blockers:** None
```

### Step 5.3: Announce Transition to User

```markdown
✅ **Stage 1 (Epic Planning) Complete**

I've created the epic structure with {N} features:

**Epic Folder:** `feature-updates/{epic_name}/`

**Features Created:**
1. feature_01_{name} - {brief purpose}
2. feature_02_{name} - {brief purpose}
3. feature_03_{name} - {brief purpose}

**Epic-Level Files:**
- EPIC_README.md (tracking and status)
- epic_smoke_test_plan.md (initial version - will update in Stages 4, 5e)
- epic_lessons_learned.md (will populate as we progress)
- research/ (shared research folder)
- GUIDE_ANCHOR.md (resumption instructions)

**Next: Stage 2 (Feature Deep Dives)**

I'll now transition to Stage 2a (Research Phase) and begin deep dive planning for Feature 1.

Starting with `stages/stage_2/phase_0_research.md` to extract epic intent, conduct targeted research, and complete research audit (Phases 0-1.5).
```

---

## 🔄 Mandatory Re-Reading Checkpoints

**CHECKPOINT 1:** After completing Phase 3 (Feature Breakdown Proposal)
- Re-read "Critical Rules" section of this guide
- Verify you presented breakdown to user (not assumed approval)
- Verify you're WAITING for user confirmation (not proceeding)
- Update EPIC_README.md Agent Status

**CHECKPOINT 2:** After creating all feature folders (Phase 4)
- Re-read "Epic Structure Creation" section
- Verify ALL required files created (README, spec, checklist, lessons learned per feature)
- Verify epic_smoke_test_plan.md marked as "INITIAL - WILL UPDATE"
- Verify GUIDE_ANCHOR.md created

**CHECKPOINT 3:** Before declaring Stage 1 complete (Phase 5)
- Re-read "Completion Criteria" section below
- Verify ALL criteria met (not just most)
- Verify EPIC_README.md updated with Stage 1 checklist marked complete

**Why this matters:** Memory degrades. Re-reading keeps you aligned with documented process.

---

## Completion Criteria

**Stage 1 is complete when ALL of these are true:**

□ Git branch created: `{work_type}/KAI-{number}`
□ EPIC_TRACKER.md updated with active epic entry
□ Initial commit made (EPIC_TRACKER.md update)
□ Epic folder created: `feature-updates/{epic_name}/`
□ Epic request moved and renamed: `{epic_name}_notes.txt`
□ EPIC_README.md created with:
  - Quick Reference Card at top
  - Agent Status section
  - Epic Overview
  - Feature Tracking table (all features listed)
  - Epic Completion Checklist (Stage 1 items checked)
□ epic_smoke_test_plan.md created and marked "INITIAL - WILL UPDATE"
□ epic_lessons_learned.md created
□ research/ folder created with README.md
□ GUIDE_ANCHOR.md created
□ Feature folders created for ALL approved features
□ Each feature folder contains:
  - README.md (with Agent Status, Completion Checklist)
  - spec.md (initial scope from Phase 3 proposal)
  - checklist.md (empty, will populate in Stage 2)
  - lessons_learned.md (template)
□ User approved feature breakdown (documented in EPIC_README.md or conversation)
□ Agent Status updated: Current Phase = DEEP_DIVE, Next Action = Read Stage 2 guide

**If any item unchecked:**
- ❌ Stage 1 is NOT complete
- ❌ Do NOT transition to Stage 2
- Complete missing items first

---

## Common Mistakes to Avoid

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll just create the folders, user will probably approve"
   ✅ STOP - Must get explicit approval first

❌ "Let me start the deep dive for Feature 1 while in Stage 1"
   ✅ STOP - Stage 1 only creates structure, Stage 2 does deep dives

❌ "This epic is simple, I'll just make one feature"
   ✅ STOP - Even simple epics benefit from feature breakdown

❌ "I'll create a detailed test plan now"
   ✅ STOP - Stage 1 test plan is placeholder, detailed plan comes in Stage 4

❌ "I remember the template structure, don't need to check"
   ✅ STOP - Always use actual template from templates/ folder

❌ "I'll update Agent Status after I finish all phases"
   ✅ STOP - Must update after EACH phase (not batched)

❌ "User seems busy, I'll assume they approve"
   ✅ STOP - Must wait for explicit approval, update Agent Status "Blockers: Waiting for user"

❌ "I'll skip GUIDE_ANCHOR.md, seems optional"
   ✅ STOP - GUIDE_ANCHOR.md is MANDATORY (critical for resumption after compaction)

❌ "The epic_smoke_test_plan.md looks incomplete, let me fill it out"
   ✅ STOP - It's SUPPOSED to be incomplete (placeholder for Stages 4, 5e)

❌ "I'll number features 1, 2, 3 (no zero-padding)"
   ✅ STOP - Must use zero-padding: 01, 02, 03 (consistent sorting)
```

---

## Real-World Examples

### Example 1: Good Feature Breakdown

**Epic Request:** "Improve draft helper with more data sources"

**GOOD Breakdown:**
```
Feature 1: ADP Integration
- Purpose: Load average draft position data from external API
- Scope: API client, data normalization, storage
- Dependencies: None (foundation)
- Estimate: ~25 items, MEDIUM risk

Feature 2: Expert Rankings Integration
- Purpose: Integrate consensus expert rankings
- Scope: Load rankings, calculate consensus, apply multiplier
- Dependencies: None (parallel to Feature 1)
- Estimate: ~20 items, LOW risk

Feature 3: Injury Risk Assessment
- Purpose: Evaluate injury history and calculate penalty
- Scope: Parse injury data, calculate risk score, apply penalty
- Dependencies: None (parallel to Features 1, 2)
- Estimate: ~15 items, LOW risk

Feature 4: Recommendation Engine Updates
- Purpose: Integrate new data sources into scoring algorithm
- Scope: Update PlayerManager, add new multipliers, integration tests
- Dependencies: Features 1, 2, 3 (consumes their outputs)
- Estimate: ~30 items, HIGH risk (integration complexity)
```

**Why GOOD:**
- Each feature delivers independent value
- Clear boundaries (data loading vs integration)
- Logical dependency chain (parallel data loading, then integration)
- Risk levels identified
- Foundation features (1, 2, 3) can be tested independently

### Example 2: Bad Feature Breakdown

**Epic Request:** "Improve draft helper with more data sources"

**BAD Breakdown:**
```
Feature 1: Data Stuff
- Purpose: Get data
- Scope: All data things
- Dependencies: None
- Estimate: Unknown

Feature 2: Calculations
- Purpose: Do the calculations
- Scope: Math and stuff
- Dependencies: Feature 1
- Estimate: Unknown

Feature 3: Miscellaneous
- Purpose: Other improvements
- Scope: Whatever's left
- Dependencies: Features 1, 2
- Estimate: Unknown
```

**Why BAD:**
- Vague purposes ("data stuff", "calculations")
- No clear boundaries (what's in Feature 1 vs 2?)
- No testability (how do you verify "math and stuff"?)
- Unknown estimates (no analysis)
- Generic "miscellaneous" feature (dumping ground)

### Example 3: Feature vs Epic Confusion

**Request:** "Add JSON export for player data"

**WRONG (treating as multi-feature epic):**
```
Feature 1: JSON Serialization
Feature 2: File Writing
Feature 3: Export Command
```

**RIGHT (single feature, not epic):**
```
This is a single feature, not an epic requiring multiple features.

Create: feature-updates/json_export_feature/
Not: feature-updates/json_export_epic/feature_01_serialization/
```

**Why:** JSON export is small, tightly coupled, <20 items. Breaking into multiple features adds unnecessary overhead.

### Example 4: Session Compaction Recovery

**Scenario:** Agent started Stage 1, then session compacted mid-Phase 3.

**WRONG Approach:**
```
"I'll just continue creating features"
(Skips re-reading guide, doesn't check Agent Status)
```

**RIGHT Approach:**
```
1. Read EPIC_README.md Agent Status
   - Sees: "Current Step: Phase 3 - Waiting for user approval"
   - Sees: "Blockers: Waiting for user confirmation of feature breakdown"

2. Read stages/stage_1/epic_planning.md (this guide)
   - Re-read Phase 3 section
   - See requirement: WAIT for approval

3. Check conversation history
   - Find: Feature breakdown was proposed
   - Find: User has NOT yet responded

4. Correct action: Continue waiting
   - Update Agent Status: "Guide Last Read: {new timestamp} (RE-READ after compaction)"
   - Do NOT proceed without approval
```

---

## README Agent Status Update Requirements

**Update Agent Status in EPIC_README.md at these points:**

1. ⚡ After Phase 1 complete (Initial Setup)
2. ⚡ After Phase 2 complete (Epic Analysis)
3. ⚡ After Phase 3 proposal presented (mark blocker: waiting for approval)
4. ⚡ After user approves breakdown (clear blocker)
5. ⚡ After Phase 4 complete (Epic Structure Created)
6. ⚡ After Phase 5 complete (Stage 1 done, ready for Stage 2)
7. ⚡ After session compaction (update "Guide Last Read" with re-read timestamp)

**Agent Status Template:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** {EPIC_PLANNING or next stage}
**Current Step:** {Exact phase and step}
**Current Guide:** stages/stage_1/epic_planning.md (or next guide)
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- {Rule 1 from Critical Rules section}
- {Rule 2 from Critical Rules section}
- {Rule 3 from Critical Rules section}

**Progress:** {X/5 phases complete in Stage 1}
**Next Action:** {Exact next task to perform}
**Blockers:** {Issues preventing progress, or "None"}

**Notes:**
- {Relevant context for next agent}
```

---

## Guide Comprehension Verification

**Before starting Stage 1, answer these questions:**

1. What must happen before creating feature folders?
   {Answer: User must approve feature breakdown}

2. Is the epic_smoke_test_plan.md complete after Stage 1?
   {Answer: No, it's a placeholder that updates in Stages 4 and 5e}

3. How many folders should be created per feature?
   {Answer: One folder per feature with 4 files: README, spec, checklist, lessons_learned}

4. When should you transition to Stage 2?
   {Answer: After ALL Phase 5 completion criteria are met and Agent Status updated}

5. What file ensures agents can resume after session compaction?
   {Answer: GUIDE_ANCHOR.md + EPIC_README.md Agent Status}

**Document your answers in EPIC_README.md notes** to prove guide comprehension.

If you cannot answer these questions without re-reading the guide, you haven't read it carefully enough.

---

## Prerequisites for Stage 2

**Before transitioning to Stage 2, verify:**

□ Stage 1 completion criteria ALL met (see "Completion Criteria" section)
□ EPIC_README.md Agent Status updated:
  - Current Phase: DEEP_DIVE
  - Current Guide: stages/stage_2/phase_0_research.md
  - Next Action: Read Stage 2a guide and begin research phase for Feature 1
□ Epic Completion Checklist: Stage 1 items all checked
□ Feature Tracking table: All features listed with "Not started" status
□ No blockers (user approval received)

**If any prerequisite fails:**
- ❌ Do NOT transition to Stage 2a
- Complete missing prerequisites
- Update Agent Status when prerequisites met

---

## Next Stage

**After completing Stage 1:**

📖 **READ:** `stages/stage_2/phase_0_research.md` (Research Phase - first of three sub-stages)
🎯 **GOAL:** Extract epic intent, conduct targeted research, pass research audit (Phases 0-1.5)
⏱️ **ESTIMATE:** 45-60 minutes (then continue with STAGE_2b and STAGE_2c)

**Stage 2 workflow (split into 3 focused guides):**
- **STAGE_2a (Research Phase):** Epic intent extraction, targeted research, research audit (Phases 0-1.5)
- **STAGE_2b (Specification Phase):** Spec with traceability, alignment check (Phases 2-2.5)
- **STAGE_2c (Refinement Phase):** Questions, scope, cross-feature alignment, user approval (Phases 3-6)

**Note:** `stages/stage_2/feature_deep_dive.md` is now a router that links to the 3 sub-stage guides.

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Stage 2a.

---

*End of stages/stage_1/epic_planning.md*
