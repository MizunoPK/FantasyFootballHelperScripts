# S1: Epic Planning Guide

🚨 **MANDATORY READING PROTOCOL**

**Before starting this guide — including when resuming a prior session:**
1. **Quick entry point:** `reference/stage_1/stage_1_reference_card.md` — use for second or later features; covers the happy path
2. **Full guide (this file):** Read entirely for your first time using this stage or when encountering edge cases
3. Acknowledge critical requirements (see "Critical Rules" section below)
4. Verify prerequisites (see "Prerequisites Checklist" section below)
5. Update epic EPIC_README.md Agent Status with guide name + timestamp

**After session compaction:**
- Check epic EPIC_README.md Agent Status for current guide
- Re-read this guide (or the reference card if in a repeat pass) before continuing
- Continue from "Next Action" in Agent Status

---

## 🚫 FORBIDDEN SHORTCUTS

You CANNOT:
- Skip Step 3 (Discovery Phase) because "the epic requirements are clear from the request file" — Discovery Phase is MANDATORY for every epic; read `s1_p3_discovery_phase.md` before Step 3
- Skip Dependency Analysis and assume all features are independent — dependency groups determine S2 parallelization and must be identified before Step 4 (Feature Breakdown Proposal)
- Propose feature breakdown (Step 4) without completing Step 2 (Epic Analysis) — Step 2 requires thorough codebase and scope analysis before breakdown

If you are about to do any of the above: STOP and re-read the relevant section.

---

## Table of Contents

1. [Overview](#overview)
2. [Critical Rules](#critical-rules)
3. [Critical Decisions Summary](#critical-decisions-summary)
4. [Prerequisites Checklist](#prerequisites-checklist)
5. [Workflow Overview](#workflow-overview)
6. [Step 0: Sibling Epic Awareness Check](#step-0-sibling-epic-awareness-check)
7. [Step 1: Initial Setup](#step-1-initial-setup)
8. [Step 2: Epic Analysis](#step-2-epic-analysis)
9. [Step 3: Discovery Phase (MANDATORY)](#step-3-discovery-phase-mandatory)
10. [Step 4: Feature Breakdown Proposal](#step-4-feature-breakdown-proposal)
11. [Step 5: Epic Structure Creation](#step-5-epic-structure-creation)
12. [Step 6: Transition to S2](#step-6-transition-to-s2)
13. [Mandatory Re-Reading Checkpoints](#mandatory-re-reading-checkpoints)
14. [Exit Criteria](#exit-criteria)
15. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
16. [README Agent Status Update Requirements](#readme-agent-status-update-requirements)
17. [Prerequisites for S2](#prerequisites-for-s2)
18. [Next Stage](#next-stage)

---

## Overview

**What is this guide?**
Epic Planning is the first stage where you create the git branch, analyze the user's epic request, conduct Discovery research, break it down into features, validate your understanding through an epic ticket, and create the folder structure for the entire epic.

**When do you use this guide?**
- User has created a request file in `.shamt/epics/requests/` with their epic request
- Starting a new epic from scratch
- Need to plan multi-feature work

**Key Outputs:**
- Git branch created for epic work
- DISCOVERY.md created and user-approved (explores problem space)
- Epic ticket created and user-validated (confirms understanding)
- Epic folder structure created (EPIC_README, epic_smoke_test_plan, feature folders)
- Initial test plan documented
- Ready to start S2 (feature deep dives)

**Time Estimate:**
2-5 hours (varies by epic size, includes Discovery Phase)

| Epic Size | Estimated Time |
|-----------|---------------|
| SMALL (1-2 features) | 2-3 hours |
| MEDIUM (3-5 features) | 3-4 hours |
| LARGE (6+ features) | 4-5 hours |

**Exit Condition:**
S1 is complete when you have Discovery approved, a validated epic ticket, complete folder structure, and user has confirmed the feature breakdown

---

## Critical Rules

```bash
+-------------------------------------------------------------+
| CRITICAL RULES - These MUST be copied to README Agent Status |
+-------------------------------------------------------------+

1. CREATE GIT BRANCH BEFORE ANY CHANGES (Step 1.0)
   - Verify on main, pull latest
   - Ask user: use next available SHAMT number or specify custom number
   - Create branch: {work_type}/SHAMT-{number}
   - Update .shamt/epics/EPIC_TRACKER.md and commit immediately

2. DISCOVERY PHASE IS MANDATORY (Step 3)
   - Every epic must go through Discovery
   - Cannot create feature folders until Discovery approved
   - Discovery informs feature breakdown
   - See: stages/s1/s1_p3_discovery_phase.md

3. DISCOVERY LOOP UNTIL 3 CONSECUTIVE CLEAN ITERATIONS
   - Continue iterating until 3 consecutive iterations produce zero new issues or gaps
   - Re-read code/requirements with fresh perspective each iteration
   - User answers questions throughout (not just at end)
   - All findings go in DISCOVERY.md

4. USER MUST APPROVE feature breakdown before creating epic ticket
   - Feature breakdown based on Discovery findings
   - User confirms/modifies
   - Do NOT proceed without approval

5. CREATE EPIC TICKET and get user validation (Steps 4.6-4.7)
   - Epic ticket validates agent understanding of outcomes
   - User must approve epic ticket before folder creation
   - Epic ticket becomes immutable reference (like epic notes)

6. Create GUIDE_ANCHOR.md in epic folder (resumption instructions)

7. epic_smoke_test_plan.md is PLACEHOLDER (will finalize in S3.P1, update in S8.P2)
   - Initial plan based on assumptions
   - Mark clearly as "INITIAL - WILL UPDATE"

8. Update EPIC_README.md Agent Status after EACH major step

9. Feature numbering: feature_01_{name}, feature_02_{name}, etc.
   - Consistent zero-padded numbering
   - Descriptive names (not generic)

10. Create research/ folder in epic root (shared across all features)

11. Epic planning does NOT include deep dives
    - S1: Discovery + structure + feature proposal
    - S2: Deep dive per feature (separate stage)

12. If unsure about feature breakdown, propose FEWER features
    - Can add features during S2
    - Harder to merge features later

13. Every feature MUST have clear purpose (1-2 sentences)
    - Avoid "miscellaneous" or "utilities" features
    - Each feature delivers distinct value

14. Mark completion in EPIC_README.md before transitioning to S2

15. TEST APPROACH IS SET ONCE AT S1 (Step 4.6.5)
    - Ask user BEFORE finalizing epic ticket (not autonomous decision)
    - Record in epic ticket AND EPIC_README header
    - Not re-decided per feature; if user changes mid-epic, document the change in EPIC_README
```

---

## Critical Decisions Summary

**S1 has 6 major decision points. Know these before starting:**

### Decision Point 1: Determine Work Type (Step 1.0d)
**Question:** Is this an epic, feat, or fix?
- **epic:** Work with multiple features (most epics)
- **feat:** Work with single feature only
- **fix:** Bug fix work
- **Impact:** Determines branch name format and EPIC_TRACKER classification

### Decision Point 2: Discovery Loop Exit (Step 3 - S1.P3.2)
**Question:** Have you completed 3 consecutive clean rounds with zero issues/gaps?
- **If NO (counter < 3):** Continue Discovery Loop - re-read with fresh perspective
- **If YES (counter = 3):** Verify exit readiness, proceed to synthesis
- **Impact:** Premature exit (counter < 3) leads to incomplete understanding; need 3 consecutive clean rounds for high confidence

### Decision Point 3: Discovery Approval (Step 3 - S1.P3.4)
**Question:** Does the user approve the Discovery findings and recommended approach?
- **If NO:** Discuss concerns, update DISCOVERY.md, re-present
- **If YES:** Proceed to feature breakdown proposal (Step 4)
- **Impact:** DISCOVERY.md becomes epic-level source of truth for all features

### Decision Point 4: Feature Breakdown Approval (Step 4)
**Question:** Does the user approve the proposed feature list?
- **If NO:** User provides feedback, agent revises breakdown
- **If YES:** Proceed to create epic ticket (Step 4.6)
- **Impact:** Defines entire epic structure - cannot easily change after folders created

### Decision Point 5: Epic Ticket Validation (Steps 4.6-4.7)
**Question:** Does the epic ticket accurately reflect user's desired outcomes?
- **If NO:** User corrects misunderstandings, agent updates epic ticket
- **If YES:** Proceed to folder creation (Step 5)
- **Impact:** Epic ticket becomes immutable reference - validates agent understanding

### Decision Point 6: Test Approach (Step 4.7)
**Question:** What automated testing approach should this epic use?
- **A. Smoke testing only** — no automated test scripts; manual E2E smoke testing at S7 and S9
- **B. Automated E2E integration scripts only** (Recommended) — runnable scripts that assert on real-data outputs; no unit tests
- **C. Unit tests for algorithmic functions only** — pure function tests; no integration scripts
- **D. Both** — algorithmic unit tests + automated E2E integration scripts
- **Impact:** Controls S3.P1 scope, S4 redirect, S5 test scope decision, S6 test gates, S7.P1 Part 3, S9 Part 4, S10 Gate 7.1/7.1b
- **Rule:** Set once at S1. If user wants to change mid-epic, agent records the update in EPIC_README with a note.
- **CRITICAL:** Agent must ask the user — this is not an autonomous decision.

**Note:** Each decision point has clear criteria. Read the detailed section before making decision.

---

## Prerequisites Checklist

**🚨 CRITICAL: Verify BEFORE starting S1 🚨**

**If you are CREATING an epic request (not starting S1):**
- ✅ Create file in `.shamt/epics/requests/{name}.md` or `.txt`
- ✅ Write comprehensive request document
- ❌ DO NOT create `SHAMT-{N}/` folder
- ❌ DO NOT create EPIC_README.md
- ❌ DO NOT create git branch
- ⏸️ STOP - Request file waits in `requests/` until user initiates S1

**If you are STARTING S1 (user explicitly said to start):**

- [ ] User has created a request file in `.shamt/epics/requests/` (check for .txt or .md file, optionally in a subfolder)
- [ ] Epic request file contains sufficient detail (problem description, goals, constraints)
- [ ] No existing epic folder with same name (check `.shamt/epics/` directory)
- [ ] Git working directory is clean (no uncommitted changes that could conflict)
- [ ] User has explicitly initiated S1 (not just asking for a request to be written)

**Parallel Play Note:** If other epics are active, S1–S5 of this epic may run in parallel with them. See the "Parallel Epic Play" section in the project rules file for the S6–S10 coordination requirement — only one agent may be in S6–S9 at a time.

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with S1
- Ask user to resolve prerequisite issue
- Document blocker in conversation

**REMEMBER:** SHAMT-{N} folders are created in Step 5 of S1, NOT before S1 starts.

---

## Workflow Overview

```text
+--------------------------------------------------------------+
|                    STAGE 1 WORKFLOW                          |
+--------------------------------------------------------------+

Step 0: Sibling Epic Awareness Check (BEFORE Step 1.0)
   +-- Read EPIC_TRACKER.md
   +-- List any epics NOT Completed or Archived (active epics)
   +-- State dependency assessment for each active epic
   +-- If any dependency found: record in EPIC_README.md ## Dependencies

Step 1: Initial Setup
   +-- Create git branch for epic (Step 1.0 - BEFORE any changes)
   |   +-- Verify on main, pull latest
   |   +-- Assign SHAMT number from .shamt/epics/EPIC_TRACKER.md
   |   +-- Create branch: {work_type}/SHAMT-{number}
   |   +-- Update .shamt/epics/EPIC_TRACKER.md and commit
   +-- Create epic folder
   +-- Note epic request file location in EPIC_README.md
   +-- Create EPIC_README.md (with Agent Status)

Step 2: Epic Analysis
   +-- Read epic request thoroughly
   +-- Identify goals, constraints, requirements
   +-- Conduct broad codebase reconnaissance
   +-- Estimate rough scope (SMALL/MEDIUM/LARGE)

Step 3: Discovery Phase (MANDATORY)
   +-- S1.P3.1: Initialize DISCOVERY.md
   +-- S1.P3.2: Discovery Loop (iterative)
   |   +-- Research (read code, examine patterns)
   |   +-- Document findings in DISCOVERY.md
   |   +-- Identify questions
   |   +-- Ask user, record answers
   |   +-- Repeat until 3 consecutive clean rounds (zero issues/gaps)
   +-- S1.P3.3: Synthesize findings
   |   +-- Compare solution options
   |   +-- Document recommended approach
   |   +-- Define scope (in/out/deferred)
   |   +-- Draft feature breakdown
   +-- S1.P3.4: User approval of Discovery
   +-- See: stages/s1/s1_p3_discovery_phase.md

Step 4: Feature Breakdown Proposal
   +-- Present feature breakdown (from Discovery)
   +-- WAIT for user confirmation/modifications
   +-- Create epic ticket (outcome validation)
   +-- WAIT for user validation of epic ticket

Step 5: Epic Structure Creation
   +-- Create feature folders (per approved breakdown)
   +-- Seed spec.md with Discovery Context
   +-- Create epic_smoke_test_plan.md (initial)
   +-- Create epic_lessons_learned.md
   +-- Create research/ folder
   +-- Create GUIDE_ANCHOR.md
   +-- Update EPIC_README.md with feature tracking table

Step 6: Transition to S2
   +-- Mark S1 complete in EPIC_README.md
   +-- Update Agent Status (next: S2)
   +-- Announce transition to user
```

---

## Step 0: Sibling Epic Awareness Check

**CRITICAL:** This check must happen BEFORE Step 1.0 — before creating your own EPIC_TRACKER entry. Reading first prevents confusing your new entry with existing active epics.

**Steps:**

1. Read `.shamt/epics/EPIC_TRACKER.md`
2. List any epics that are **NOT** marked Completed or Archived (i.e., any active or unfinished epic, regardless of the exact status label used)
3. For each active epic, state explicitly:
   - "This new epic **[does / does not]** depend on work from **[epic name]**, because **[reason]**"
4. If any dependency exists: note it now — you will record it in `EPIC_README.md` under `## Dependencies` when creating that file in Step 1.3.

**If no active epics exist:** Note "No active epics — no dependency check needed" and proceed to Step 1.0.

**Why before Step 1.0:** Discovering a dependency at S5 or S6 is far more expensive than at creation time. A single read + short reasoning step at S1 prevents plan invalidation later.

---

## Step 1: Initial Setup

### Step 1.0: Create Git Branch for Epic

**CRITICAL:** Create branch BEFORE making any changes to codebase.

**Steps:**
1. Verify you're on main branch (`git checkout main`)
2. Pull latest changes (`git pull origin main`)
3. Read .shamt/epics/EPIC_TRACKER.md to identify "Next Available Number"
4. **Ask user for SHAMT number preference** (use AskUserQuestion):
   - Option A: Use next available number (e.g., SHAMT-9) - Recommended
   - Option B: Specify custom SHAMT number (user provides number)
   - **Rationale:** Allows user control over epic numbering for organizational purposes
5. Determine work type (epic/feat/fix) - typically "epic" for multi-feature work
6. Create and checkout branch (`git checkout -b {work_type}/SHAMT-{number}`)
7. Update .shamt/epics/EPIC_TRACKER.md (add to Active table, increment next number if using next available)
8. Commit .shamt/epics/EPIC_TRACKER.md update immediately

**Why branch first:** Keeps main clean, allows parallel work, enables rollback

**Example: Asking for SHAMT number preference**

After reading .shamt/epics/EPIC_TRACKER.md showing "Next Available Number: SHAMT-9", use AskUserQuestion:

```text
Question: "Which SHAMT number should I use for this epic?"
Header: "SHAMT Number"
Options:
  - Option A: "Use next available (SHAMT-9)" (Recommended)
    Description: "Uses the next sequential number from .shamt/epics/EPIC_TRACKER.md"
  - Option B: "Specify custom number"
    Description: "You provide a specific SHAMT number (e.g., for organizational grouping)"
```

If user selects Option B, they will provide the custom number in "Other" text input.

---

### Step 1.1: Create Epic Folder

Create epic folder: `.shamt/epics/SHAMT-{N}-{epic_name}/`

**Naming:** Use SHAMT number + snake_case epic name (e.g., `SHAMT-1-improve_recommendation_engine`)

### Step 1.2: Move Epic Request File into Epic Folder

Find the request file in `.shamt/epics/requests/` (check subfolders if needed). Move it into the epic folder:

```bash
mv .shamt/epics/requests/{filename} .shamt/epics/SHAMT-{N}-{epic_name}/
```

Note the new path in `EPIC_README.md` so it's easy to find.

### Step 1.3: Create EPIC_README.md

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "Epic README Template"

Include Agent Status section with: Current Phase (EPIC_PLANNING), Current Step (Step 1 complete), Current Guide, Critical Rules, Progress (1/5), Next Action (Step 2).

### Step 1.4: Update Agent Status

Update Agent Status after Phase 1 completion.

---

## Step 2: Epic Analysis

**Goal:** Understand epic request and identify major components

**DO NOT:**
- ❌ Jump to implementation details
- ❌ Deep dive into specific features (that's S2)
- ❌ Write code or create detailed specs

**DO:**
- ✅ Read epic request thoroughly (multiple times)
- ✅ Identify high-level goals and constraints
- ✅ Conduct broad codebase reconnaissance
- ✅ Understand existing patterns to leverage

### Step 2.1: Read Epic Request Thoroughly

Read `{epic_name}_notes.txt` and identify:
1. What problem is being solved?
2. What are the explicit goals?
3. What constraints are mentioned?
4. What's explicitly OUT of scope?

### Step 2.2: Identify Major Components Affected

Conduct quick searches to find which managers/classes/modules will be affected. Document components likely affected and similar existing features to reference.

### Step 2.3: Estimate Rough Scope

Tag epic as SMALL (1-2 features), MEDIUM (3-5 features), or LARGE (6+ features). Add Initial Scope Assessment to EPIC_README.md with size, complexity, risk level, estimated components.

### 🚨 Epic Size Check (MANDATORY if LARGE)

**If the epic is LARGE (6+ features), pause and recommend splitting to the user before continuing.**

An epic with 6+ features is likely too large to complete reliably in a single epic lifecycle:
- Sessions run out of context mid-execution, causing continuity problems across agents
- Coordination overhead grows significantly with feature count
- Later features frequently don't get implemented before the epic is abandoned
- Users lose track of overall progress when epics span many weeks

**Recommended conversation with user:**
> "This epic appears to have {N} features, which exceeds the recommended maximum of 5.
> I suggest splitting it into two smaller epics:
> - Epic A: Features 1-{M} (foundational work / Wave 1)
> - Epic B: Features {M+1}-{N} (extended work / Wave 2)
>
> Smaller epics complete faster, are easier to track, and have much higher completion rates.
> Would you like to split into two epics, or proceed with all {N} features in one epic?"

**If user chooses to split:** Stop S1, help user create two new epic request .txt files, then begin S1 for the first epic.

**If user chooses to proceed with 6+ features:** Document the decision explicitly in EPIC_README.md under the Initial Scope Assessment section: "Note: User chose to proceed with {N} features (exceeds recommended maximum of 5). Increased compaction risk acknowledged."

### Step 2.4: Update Agent Status

After Step 2:
- Progress: "2/6 steps complete (Epic Analysis)"
- Next Action: "Step 3 - Discovery Phase"

---

## Step 3: Discovery Phase (MANDATORY)

**🚨 CRITICAL:** Discovery Phase is MANDATORY for every epic. Cannot create feature folders until Discovery is complete and user-approved.

**Goal:** Explore problem space through iterative research and user Q&A before proposing feature breakdown.

**Time-Box by Epic Size:**
| Epic Size | Discovery Time |
|-----------|---------------|
| SMALL (1-2 features) | 1-2 hours |
| MEDIUM (3-5 features) | 2-3 hours |
| LARGE (6+ features) | 3-4 hours |

**Exit Condition:** Discovery Loop exits when 3 CONSECUTIVE research iterations produce zero new issues or gaps.

**Key Outputs:** DISCOVERY.md (source of truth), solution approach, scope definition, feature breakdown draft

**📖 READ ENTIRE GUIDE:** `stages/s1/s1_p3_discovery_phase.md`

The detailed guide contains:
- S1.P3.1: Initialize DISCOVERY.md
- S1.P3.2: Discovery Loop (iterative research, questions, user answers)
- S1.P3.3: Synthesize Findings (compare options, define scope, draft features)
- S1.P3.4: User Approval

**After Discovery approved:** Proceed to Step 4 with feature breakdown drafted.

---

## Step 4: Feature Breakdown Proposal

**Goal:** Formalize the feature breakdown from Discovery (user must approve)

**Note:** Feature breakdown was drafted during Discovery Phase (S1.P3.3). This step formalizes and validates it.

### Step 4.1: Present Feature Breakdown

Present the feature breakdown from DISCOVERY.md to user for formal approval.

**Include in presentation:**
- Feature list with purpose, scope, dependencies
- Discovery basis for each feature (which findings/answers informed it)
- Recommended implementation order
- Request for user confirmation

**See:** `reference/stage_1/feature_breakdown_patterns.md` for:
- Common breakdown patterns (data pipeline, algorithm, multi-source, etc.)
- Decision trees for determining number of features
- Split vs combine decision framework

### Step 4.2: WAIT for User Approval

**STOP HERE - Do NOT proceed without user confirmation**

**DO NOT:**
- Create feature folders yet
- Assume user agrees
- Start S2 deep dives

**DO:**
- Wait for user response
- Update EPIC_README.md Agent Status: "Blockers: Waiting for user approval of feature breakdown"
- Be ready to modify proposal based on user feedback

### Step 4.3: Incorporate User Feedback

**If user requests changes:**
1. Revise feature breakdown based on feedback
2. Update DISCOVERY.md if scope changes
3. Present revised breakdown
4. Wait for approval again

**If user approves:**
1. Document approval in EPIC_README.md
2. Proceed to Step 4.6 (Epic Ticket Creation)

---

### Step 4.6: Create Epic Ticket (Outcome Validation)

**Purpose:** Validate agent understands epic outcomes and acceptance criteria BEFORE creating folder structure

**Why this matters:** Catches epic-level misinterpretation early, preventing 40+ hours of work in wrong direction

**Process:**

1. **Draft epic ticket** using template from reference guide
   - Use the "Definition of Done" section of the epic request as the starting point — pull `Success looks like` and `Failure looks like` entries directly as initial acceptance criteria and failure patterns, then refine based on Discovery findings
2. **Save to:** `.shamt/epics/{epic_name}/EPIC_TICKET.md`
3. **Present to user** for validation
4. **Proceed to Step 4.7** for user sign-off

**📖 See:** `reference/stage_1/epic_planning_examples.md` → "Example 7: Epic Ticket Template" for:
- Complete epic ticket template
- Guidelines for description, acceptance criteria, success indicators, failure patterns
- Real-world example (Feature 02 epic ticket)

---

### Step 4.6.5: Test Approach Decision (MANDATORY — ask user before finalizing ticket)

**Purpose:** Set the epic's testing approach once, before folder creation. This decision controls behavior across S3, S5, S6, S7, S9, and S10.

**Process:**

1. Before finalizing the epic ticket, ask the user (use AskUserQuestion):

```text
"What automated testing approach should this epic use?"

A. Smoke testing only — no automated test scripts; manual E2E smoke testing at S7 and S9
B. Automated E2E integration scripts only (Recommended) — runnable scripts that assert on
   real-data outputs; no unit tests
C. Unit tests for algorithmic functions only — pure function tests; no integration scripts
D. Both — algorithmic unit tests + automated E2E integration scripts
```

2. Record the user's answer in two places (before presenting ticket for validation):
   - Add `Testing Approach: [A/B/C/D — description]` to the epic ticket draft
   - Add `Testing Approach: [A/B/C/D — description]` to EPIC_README header block
   - For Options B or D, also add `Integration Test Convention: [TBD — will be set in S5]` to EPIC_README header

3. **Critical rule:** This preference is set once at S1. It is not re-decided per feature. If the user wants to change it mid-epic, record the update in EPIC_README with a change note.

---

### Step 4.7: User Validation of Epic Ticket

**STOP HERE - Do NOT proceed without user validation**

**Present epic ticket to user:**

```markdown
## Epic Ticket Validation Checkpoint

I've created an epic ticket to validate my understanding of the epic's goals and acceptance criteria.

**Location:** `.shamt/epics/{epic_name}/EPIC_TICKET.md`

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
   - [x] Epic ticket created and user-validated (Step 4.7)
   ```
2. Epic ticket is now **immutable reference** (like epic notes)
3. Proceed to Step 5

**Critical:** Epic ticket becomes source of truth for outcomes. During S5 v2 Validation Loop (Dimension 11: Spec Alignment), implementation_plan.md will be validated against spec.md, which was validated against both epic notes AND epic ticket.

---

## Step 5: Epic Structure Creation

**Prerequisites:**
- User has approved Discovery findings (Step 3)
- User has approved feature breakdown (Step 4)
- User has validated epic ticket (Step 4.7)

### Step 5.1: Create Feature Folders

For EACH approved feature, create folder: `.shamt/epics/SHAMT-{N}-{epic_name}/feature_{NN}_{name}/`

**Naming:** Zero-padded numbers + descriptive snake_case name (e.g., `feature_01_rank_integration`)

**For each feature folder, create 4 files:**
1. **README.md** - Use Feature README Template (Agent Status: PLANNING phase)
2. **spec.md** - Seed with Discovery Context section (see below), copy purpose/scope from DISCOVERY.md
3. **checklist.md** - Empty (will populate in S2)
4. **lessons_learned.md** - Template with empty sections

### Step 5.1a: Seed spec.md with Discovery Context

Each feature's spec.md starts with Discovery Context section:

```markdown
## Feature Spec: {feature_name}

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)
{Copy from DISCOVERY.md Proposed Feature Breakdown section}

### Relevant Discovery Decisions
- **Solution Approach:** {From DISCOVERY.md Recommended Approach}
- **Key Constraints:** {Constraints affecting this feature}
- **Dependencies:** {From DISCOVERY.md feature dependencies}

### Relevant User Answers (from Discovery)
| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| {Q from Discovery} | {A} | {How it affects this feature} |

---

## Feature Requirements
{To be completed in S2}
```

### Step 5.2: Create epic_smoke_test_plan.md

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "Epic Smoke Test Plan Template"

**IMPORTANT:** Mark this as INITIAL VERSION (placeholder that will be finalized in S3.P1, updated in S8.P2)

**Key characteristics of initial version:**
- Based on assumptions from epic request (no implementation knowledge yet)
- Rough guesses for test commands/scenarios
- High-level success criteria (will be refined)
- Marked clearly as "INITIAL - WILL UPDATE"

### Step 5.3: Create epic_lessons_learned.md

Create template file with sections for Planning Phase Lessons, Implementation Phase Lessons, QC Phase Lessons, and Guide Improvements Identified (all empty - will populate during workflow).

### Step 5.4: Create research/ Folder

Create `research/` folder in epic root with README.md explaining purpose (centralizes research/analysis documents, keeps epic root clean).

**Note:** Discovery Phase may have already created research files in this folder during S1.P3.

### Step 5.5: Create GUIDE_ANCHOR.md

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "GUIDE_ANCHOR Template"

**Critical sections:**
- Instructions for resuming after session compaction
- Current stage identification
- Active guide name
- Workflow reference diagram

**This file ensures agents can resume correctly after context window limits.**

### Step 5.6: Update EPIC_README.md

Add **Feature Tracking** table listing all features with S2 Complete and S8.P2 Complete checkboxes (all unchecked initially).

Add **Epic Completion Checklist** with all 10 stages (S1 items checked, all others unchecked).

### Step 5.7: Update Agent Status

Update Agent Status: Progress 5/6, Next Action "Step 5.7.5 - Feature Dependency Analysis", list features created.

---

### Step 5.7.5: Analyze Feature Dependencies

**Purpose:** Identify spec-level dependencies to determine S2 wave order for group-based parallelization

**For EACH feature:**

1. **Spec Dependencies (matters for S2 parallelization):**
   - Does this feature need other features' SPECS to write its own spec?
   - Example: Feature B needs to know Feature A's API to write integration spec
   - → Creates S2 dependency (Feature A must complete S2 before Feature B starts)

   **🚨 Use the DEEP CHECK, not the shallow check:**
   - ❌ Shallow check (WRONG): "Can I identify WHAT to build from Discovery?"
   - ✅ Deep check (CORRECT): "Can I write a COMPLETE spec without knowing upstream's output structure?"

   **Ask for EACH feature:**
   - a. What is the output/interface that the upstream feature will define in S2?
   - b. Does MY spec need to describe how I use that interface?
   - c. Is that interface fully defined in Discovery, or will it be defined in upstream's S2?
   - d. **If the interface will be defined in upstream's S2 → spec-level dependency exists**

   **Common patterns that indicate spec-level dependency:**
   - "My feature wires CLI args into [upstream's refactored constructors/APIs]" → SPEC DEP
   - "My feature calls [upstream's functions/endpoints] that don't exist yet" → SPEC DEP
   - "My feature's behavior depends on decisions upstream is making in S2" → SPEC DEP

   **⚠️ Special Cases — Almost Always Have Spec Dependencies:**
   - **Integration features** (e.g., "integrate X with Y") — need both X and Y specs
   - **Test/framework features** (e.g., "integration test framework", "test runner") — need specs of what they test
   - **Orchestration features** (e.g., "master runner", "pipeline coordinator") — need specs of what they orchestrate
   - **Wrapper/adapter features** (e.g., "CLI wrapper for existing API") — need the upstream API spec

   For these feature types, default assumption is **SPEC DEPENDENCY EXISTS** unless you can prove otherwise.

2. **Implementation Dependencies (matters for S5-S8, NOT S2):**
   - Does this feature need other features' CODE to build its implementation?
   - Example: Feature B calls Feature A's functions
   - → Creates S5 dependency (Feature A must complete S5-S8 before Feature B starts)
   - → Does NOT affect S2 parallelization (both can research/specify in parallel)

**Decision Criteria for Grouping:**
- **Spec-level dependency → Different group** (affects S2 parallelization)
- **Implementation dependency only → Same group** (doesn't affect S2)
- **No dependencies → Group 1** (can parallelize freely)

**Historical Warning (SHAMT-10):**
Features 02-08 were placed in the same group as Feature 01. They could identify WHAT CLI args to add (from Discovery) but could NOT write a complete spec for HOW those args wire through Feature 01's refactored constructors — because Feature 01 was actively defining those constructors in its own S2. All 7 secondary agents had to be paused mid-S2 and the epic restructured into 3 waves. Use the deep check above to prevent this.

**Organize into Groups:**

**Group 1 (Foundation - S2 Wave 1):**
- Features with NO spec-level dependencies
- Can research and specify independently
- Will complete S2 first (provides API reference for dependent features)

**Group 2 (Dependent - S2 Wave 2):**
- Features that need Group 1's specs as reference
- Must wait for Group 1 to complete S2
- Will do S2 in parallel with each other once Group 1 done

**Group 3+ (if needed):**
- Features that need Group 2's specs
- Continue wave pattern (each wave waits for previous wave's S2 completion)

**Document in EPIC_README.md:**

```markdown
## Feature Dependency Groups (S2 Only)

**Group 1 (Foundation - S2 Wave 1):**
- Feature 01: {name}
- Spec Dependencies: None
- S2 Workflow: Completes S2 alone FIRST

**Group 2 (Dependent - S2 Wave 2):**
- Features 02-07: {names}
- Spec Dependencies: Need Group 1's spec (API reference)
- S2 Workflow: After Group 1 completes S2, all features do S2 in parallel

**After S2:**
- Groups no longer matter
- S3: Epic-level (all features together)
- S4: Per-feature sequential
- S5-S8: Per-feature sequential (implementation dependencies checked separately)
- S9-S10: Epic-level

**S2 Workflow:**
- **Wave 1:** Group 1 completes S2 (S2.P1 + S2.P2)
- **Wave 2:** Group 2 does S2 in parallel (after Group 1 S2 complete)
- **Wave 3+:** Continue pattern if more groups exist
- **After all waves:** Groups no longer matter, proceed to S3

**S2 Time Savings:**
- Sequential S2: {N} features × 2h = {total}h
- Group-based S2: Wave 1 ({M}h) + Wave 2 parallel ({M}h) = {total}h
- Savings: {X}h ({percent}% reduction)
```

**If all features independent:** Note "All features independent - Single S2 wave" and place all features in Group 1

---

### CHECKPOINT: Parallelization Assessment Gate

**STOP HERE if epic has 2+ features.**

Before proceeding to Step 6, you MUST complete Steps 5.8-5.9.

**Checklist:**
- [ ] Feature count verified (if 1 feature, skip to Step 6)
- [ ] If 2+ features: Step 5.8 analysis completed
- [ ] If 3+ features: Step 5.9 offer presented to user
- [ ] User response documented (parallel enabled OR sequential chosen)

**DO NOT proceed to Step 6 until this checkpoint satisfied.**

---

### Step 5.8: Analyze Features for Parallelization

**Purpose:** Determine if S2 parallelization should be offered

**When to analyze:** Epic has 2+ features, before transitioning to S2

**Analysis:**
1. **Count features** and calculate savings:
   - Sequential S2: N features x 2 hours = X hours
   - Parallel S2: 2 hours (simultaneous execution)
   - Savings: X - 2 hours

2. **Time savings examples:**
   - 2 features: Save 2 hours (50%)
   - 3 features: Save 4 hours (67%)
   - 4 features: Save 6 hours (75%)

**Decision Criteria:**
- **OFFER parallel** if: 3+ features OR 2 features + user time-constrained
- **SKIP parallel** if: 1 feature OR modest savings + user prefers simplicity

**If offering:** Proceed to Step 5.9
**If skipping:** Skip to Step 6

### Step 5.9: Offer Parallel Work to User

**Prerequisites:** Analysis shows 2+ features, decision made to offer parallelization

**Determine Offering Type:**
- **Group-Based:** Epic has dependency groups (check EPIC_README.md "Feature Dependency Groups (S2 Only)" section)
- **All Independent:** All features in single group OR no spec-level dependencies

---

#### Offering Template A: Group-Based Parallelization

**Use when:** Epic has multiple dependency groups (Group 1, Group 2, etc.)

```markdown
🚀 PARALLEL WORK OPPORTUNITY

I've identified {N} features organized into {M} dependency groups:

**Group 1 (Foundation):**
- Feature {X}: {name}
- No dependencies, completes S2 first

**Group 2 (Dependent):**
- Features {Y}-{Z}: {names}
- Depend on Group 1's spec (need API reference)
- Can parallelize with each other once Group 1 done

**Sequential approach:**
- All {N} features one-by-one: {total} hours

**Group-based parallel approach:**
- Group 1 completes S2: {M} hours
- Group 2 does S2 in parallel ({K} features): {M} hours
- Total: {total} hours

**TIME SAVINGS: {X} hours ({percent}% reduction in S2 time)**

**Workflow:**
1. I complete S2 for Group 1 (Feature {X})
2. After Group 1 done → I spawn {K} secondary agents for Group 2
3. All {K} Group 2 features do S2 simultaneously
4. After all S2 complete → I run S3 (epic-level)

**Coordination:**
- You'll open {K} additional Claude Code sessions (when Group 1 done)
- I'll coordinate all agents via files
- Group 1 completes before Group 2 starts (dependency requirement)

Would you like to:
1. ✅ Enable group-based parallel work (I'll coordinate)
2. ❌ Continue sequential (I'll do all {N} one-by-one)
3. ❓ Discuss approach
```

---

#### Offering Template B: All Features Independent

**Use when:** All features have no dependencies OR single group

```markdown
🚀 PARALLEL WORK OPPORTUNITY

I've identified {N} features with no dependencies - all can parallelize!

**Sequential approach:**
- All {N} features one-by-one: {total} hours

**Parallel approach:**
- All {N} features simultaneously: 2 hours

**TIME SAVINGS: {X} hours ({percent}% reduction in S2 time)**

**Workflow:**
1. I spawn {N-1} secondary agents immediately
2. I work on Feature 01, secondaries work on Features 02-{N}
3. All {N} features do S2 simultaneously
4. After all S2 complete → I run S3 (epic-level)

**Coordination:**
- You'll open {N-1} additional Claude Code sessions
- I'll coordinate all agents via files

Would you like to:
1. ✅ Enable parallel work (I'll coordinate)
2. ❌ Continue sequential (I'll do all {N} one-by-one)
3. ❓ Discuss approach
```

---

#### Offering Template C: Wave 1 Precedent Pattern

**Use when:** Epic has 3+ features all implementing the SAME architectural pattern, where one representative feature should go first to establish concrete design decisions (class structure, constructor signatures, naming conventions) before others begin.

**When to recognize this pattern:**
- All features apply the same refactoring approach to different modules (e.g., "add argparse + DI to all 7 runner scripts")
- Pattern requires upfront decisions with multiple valid options (dataclass vs pydantic, subprocess vs direct import, naming conventions)
- Features are code-independent from each other (no import chain between them)
- Getting one feature "right first" would make the remaining features much clearer to spec

```markdown
🚀 WAVE 1 PRECEDENT OPPORTUNITY

I've identified {N} features that all implement the same architectural pattern.
I suggest a "Wave 1 Precedent" approach rather than full parallelization:

**Wave 1 (Solo — establishes design decisions):**
- Feature {X}: {name} — most representative/complex example
- Completes S2 + S5 + S6 + S7 + S8 FULLY before Wave 2 begins
- Documents all design decisions as "established precedents"

**Wave 2 (Parallel — uses Wave 1 as template):**
- Features {Y}-{Z}: {names}
- Execute S2 in parallel, each referencing Wave 1's spec as starting point
- Resolved design decisions from Wave 1 carry forward automatically

**Why this over full parallelization:**
- Prevents {N} agents making different design decisions independently
- Wave 2 handoffs say "use Feature {X}'s pattern" — much simpler than re-speccing
- Cross-feature conflicts in S3 are greatly reduced (Wave 2 already aligned)

**Time profile:**
- Wave 1 solo: ~{M} hours (S2+S5+S6+S7+S8 for Feature {X})
- Wave 2 parallel S2: ~2 hours
- Total: ~{M+2} hours (vs {N}×2 hours sequential)

Would you like to:
1. ✅ Use Wave 1 Precedent approach (Feature {X} first, then parallel Wave 2)
2. 🔀 Use full parallelization (all features S2 simultaneously — design decisions split)
3. ❌ Continue sequential (all {N} features one-by-one)
4. ❓ Discuss approach
```

**Handle User Response:**
- **Option 1 (Wave 1 Precedent):** Complete S2-S8 for Wave 1 feature solo, then spawn secondaries for Wave 2 S2 using `s2_primary_agent_group_wave_guide.md`
- **Options 2-3:** See existing handling above

---

**Handle User Response (Templates A and B):**
- **Option 1 (Enable):** Skip Step 6, go to `parallel_work/s2_primary_agent_guide.md` (groups) or standard parallel guide (no groups)
- **Option 2 (Sequential):** Proceed to Step 6 (standard transition)
- **Option 3 (Discuss):** Answer questions, clarify groups/workflow, then re-present options 1-2

**Notes:** Parallel work is OPTIONAL, user chooses, default to sequential if unclear

---

## Step 6: Transition to S2

### Step 6.1: Mark S1 Complete

Check all S1 items in EPIC_README.md Epic Completion Checklist.

### Step 6.2: Determine S2 Workflow Mode

**Check EPIC_README.md for parallelization decision:**

**Scenario A: Group-Based Parallel S2** (epic has dependency groups, user accepted parallel work)
- Epic has "Feature Dependency Groups (S2 Only)" section with multiple groups
- User selected "Enable group-based parallel work"
- → Group wave workflow

**Scenario B: All Features Independent Parallel** (no dependency groups, user accepted parallel work)
- All features in single group OR no spec-level dependencies
- User selected "Enable parallel work"
- → Full parallelization workflow

**Scenario C: Sequential S2** (user declined parallel work OR only 1-2 features)
- User selected "Continue sequential"
- OR epic has only 1-2 features (parallel not offered)
- → Sequential workflow

### Step 6.3: Update Agent Status for S2

**For Scenario A (Group-Based Parallel):**

Update Agent Status:
- Current Phase: "DEEP_DIVE_GROUP_1"
- Current Guide: "stages/s2/s2_feature_deep_dive.md" (will route to group wave guide)
- Next Action: "Read S2 router guide and begin Group 1 S2 execution"
- Groups: "Group 1 first, Group 2 after Group 1 S2 complete"

**For Scenario B (All Independent Parallel):**

Update Agent Status:
- Current Phase: "DEEP_DIVE_PARALLEL"
- Current Guide: "parallel_work/s2_primary_agent_guide.md"
- Next Action: "Generate handoff packages for {N-1} secondary agents"

**For Scenario C (Sequential):**

Update Agent Status:
- Current Phase: "DEEP_DIVE"
- Current Guide: "stages/s2/s2_feature_deep_dive.md"
- Next Action: "Read S2.P1 guide and begin research for feature_01_{name}"

### Step 6.4: Announce Transition to User

**For Group-Based Parallel:**

```markdown
✅ S1 Complete! Transitioning to S2 with group-based parallelization.

**Groups:**
- Group 1 (Foundation): Feature {X}
- Group 2 (Dependent): Features {Y}-{Z}

**Workflow:**
1. Starting with Group 1 (Feature {X})
2. I'll complete S2 for Feature {X} first (S2.P1 + S2.P2)
3. After Group 1 S2 complete → I'll spawn {K} secondary agents
4. Group 2 ({K} features) will do S2 in parallel
5. After all S2 complete → I'll run S3

**Estimated Time:**
- Group 1 S2: 2 hours
- Group 2 S2 (parallel): 2 hours
- Total: 4 hours (vs {X} hours sequential)

**Next Action:** Reading S2 router guide and beginning Group 1 S2
```

**For All Independent Parallel:**

```markdown
✅ S1 Complete! Transitioning to S2 with full parallelization.

**All {N} features are independent - can parallelize immediately!**

I'll now generate handoff packages for {N-1} secondary agents...

**Next Action:** Generating handoff packages
```

**For Sequential:**

```markdown
✅ S1 Complete! Transitioning to S2 (sequential mode).

I'll work through all {N} features one-by-one, starting with Feature 01.

**Next Action:** Beginning S2.P1 for Feature 01
```

---

## Mandatory Re-Reading Checkpoints

## 🛑 MANDATORY CHECKPOINT 1

**You have completed Step 2 (Epic Analysis)**

⚠️ STOP - DO NOT PROCEED TO STEP 3 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Discovery Phase" section of this guide
2. [ ] Verify you understand Discovery Loop exit condition
3. [ ] Update EPIC_README.md Agent Status:
   - Current Step: "S1 Step 2 complete, starting S1.P3 Discovery Phase"
   - Last Updated: [timestamp]
4. [ ] Output acknowledgment: "✅ CHECKPOINT 1 COMPLETE: Re-read Discovery Phase section"

**ONLY after completing ALL 4 actions above, proceed to Step 3 (Discovery Phase)**

---

## 🛑 MANDATORY CHECKPOINT 2

**You have completed Step 3 (Discovery Phase)**

⚠️ STOP - DO NOT PROCEED TO STEP 4 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Feature Breakdown Proposal" section of this guide
2. [ ] Verify DISCOVERY.md is complete and user-approved
3. [ ] Verify feature breakdown is based on Discovery findings
4. [ ] Update EPIC_README.md Agent Status:
   - Current Step: "S1.P3 complete, starting S1 Step 4 (Feature Breakdown)"
   - Last Updated: [timestamp]
5. [ ] Output acknowledgment: "✅ CHECKPOINT 2 COMPLETE: Re-read Feature Breakdown section, verified Discovery approved"

**ONLY after completing ALL 5 actions above, proceed to Step 4 (Feature Breakdown)**

---

## 🛑 MANDATORY CHECKPOINT 3

**You have completed Step 4 (Feature Breakdown)**

⚠️ STOP - DO NOT PROCEED TO STEP 5 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Epic Structure Creation" section of this guide
2. [ ] Verify epic ticket created and user-validated
3. [ ] Update EPIC_README.md Agent Status:
   - Current Step: "S1 Step 4 complete, starting S1 Step 5 (Epic Structure)"
   - Last Updated: [timestamp]
4. [ ] Output acknowledgment: "✅ CHECKPOINT 3 COMPLETE: Re-read Epic Structure section, verified epic ticket validated"

**ONLY after completing ALL 4 actions above, proceed to Step 5 (Epic Structure Creation)**

---

## 🛑 MANDATORY CHECKPOINT 4

**You have completed Step 5 (Epic Structure Creation)**

⚠️ STOP - DO NOT PROCEED TO STEP 6 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read Step 5 section of this guide
2. [ ] Verify ALL required files created:
   - [ ] Epic-level: README, DISCOVERY, test plan, lessons learned, research/, GUIDE_ANCHOR
   - [ ] Each feature: README, spec with Discovery Context, checklist, lessons learned
3. [ ] Verify spec.md has Discovery Context section populated
4. [ ] Verify epic_smoke_test_plan.md marked as "INITIAL - WILL UPDATE"
5. [ ] Verify GUIDE_ANCHOR.md created
6. [ ] Update EPIC_README.md Agent Status:
   - Current Step: "S1 Step 5 complete, starting S1 Step 6 (Final Verification)"
   - Last Updated: [timestamp]
7. [ ] Output acknowledgment: "✅ CHECKPOINT 4 COMPLETE: Re-read Step 5, verified all files created"

**ONLY after completing ALL 7 actions above, proceed to Step 6 (Final Verification)**

---

## 🛑 MANDATORY CHECKPOINT 5

**You are about to declare S1 complete**

⚠️ STOP - DO NOT PROCEED TO S2 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Completion Criteria" section below
2. [ ] Verify ALL completion criteria met (see checklist below)
3. [ ] Verify EPIC_README.md updated with S1 checklist marked complete
4. [ ] Update EPIC_README.md Agent Status:
   - Current Guide: "stages/s2/s2_feature_deep_dive.md"
   - Current Step: "Ready to start S2.P1 for Feature 01"
   - Last Updated: [timestamp]
5. [ ] Output acknowledgment: "✅ CHECKPOINT 5 COMPLETE: All S1 completion criteria verified, ready for S2"

**ONLY after completing ALL 5 actions above, proceed to S2**

---

---

## Exit Criteria

**S1 is complete when ALL of these are true:**

[ ] Sibling epic awareness check completed (Step 0) — any dependencies noted for EPIC_README.md
[ ] Git branch created and .shamt/epics/EPIC_TRACKER.md updated
[ ] DISCOVERY.md created and user-approved
[ ] Epic folder structure complete (EPIC_README, DISCOVERY, test plan, lessons learned, research/, GUIDE_ANCHOR)
[ ] Feature folders created with 4 files each (README, spec with Discovery Context, checklist, lessons learned)
[ ] User approved Discovery findings (Step 3)
[ ] User approved feature breakdown (Step 4)
[ ] Testing Approach (A/B/C/D) set in EPIC_README and epic ticket (Step 4.6.5)
[ ] User validated epic ticket (Step 4.7)
[ ] Agent Status updated for S2 transition

**If any item unchecked:** Do NOT transition to S2

---

## Common Mistakes to Avoid

```text
+------------------------------------------------------------+
| "If You're Thinking This, STOP" - Anti-Pattern Detection   |
+------------------------------------------------------------+

X "This epic seems clear, I'll skip Discovery"
  --> STOP - Discovery is MANDATORY for every epic, no exceptions

X "I found no questions in the first research round, Discovery done"
  --> STOP - Continue researching until truly no questions; one round is rarely enough

X "I'll propose features now and do Discovery after"
  --> STOP - Discovery MUST complete before feature breakdown

X "I'll just create the folders, user will probably approve"
  --> STOP - Must get explicit approval first

X "Let me start the deep dive for Feature 1 while in S1"
  --> STOP - S1 only creates structure, S2 does deep dives

X "This epic is simple, I'll just make one feature"
  --> STOP - Even simple epics go through Discovery + feature breakdown

X "I'll create a detailed test plan now"
  --> STOP - S1 test plan is placeholder, detailed plan comes in S3.P1 (updated in S8.P2)

X "I remember the template structure, don't need to check"
  --> STOP - Always use actual template from templates/ folder

X "I'll update Agent Status after I finish all steps"
  --> STOP - Must update after EACH step (not batched)

X "User seems busy, I'll assume they approve"
  --> STOP - Must wait for explicit approval, update Agent Status "Blockers: Waiting for user"

X "I'll skip GUIDE_ANCHOR.md, seems optional"
  --> STOP - GUIDE_ANCHOR.md is MANDATORY (critical for resumption after compaction)

X "The epic_smoke_test_plan.md looks incomplete, let me fill it out"
  --> STOP - It's SUPPOSED to be incomplete (placeholder for S3.P1, updated in S8.P2)

X "I'll number features 1, 2, 3 (no zero-padding)"
  --> STOP - Must use zero-padding: 01, 02, 03 (consistent sorting)

X "I'll skip seeding spec.md with Discovery Context"
  --> STOP - Every spec.md MUST start with Discovery Context section

X "I'll create a documentation feature to update README/ARCHITECTURE"
  --> STOP - Documentation is handled in S7.P3 (per-feature) and S10 (epic-level), NOT as separate feature
  --> EXCEPTION: Only create documentation feature if user EXPLICITLY requests it

X "I'll decide the testing approach myself (Option B seems fine)"
  --> STOP - Test approach is NOT an autonomous decision; must ask user via AskUserQuestion at Step 4.6.5

X "I'll set the testing approach per-feature based on what makes sense for each one"
  --> STOP - Testing approach is set ONCE at S1 for the entire epic, not per feature
```

**📖 See:** `reference/stage_1/epic_planning_examples.md` for:
- Example 1-4: Real-world feature breakdown examples (good vs bad)
- Example 5: Epic ticket example
- Example 6: Multi-feature epic analysis walkthrough
- Example 7-10: Additional patterns and scenarios

---

## README Agent Status Update Requirements

**Update Agent Status in EPIC_README.md at these points:**

1. After Step 1 complete (Initial Setup)
2. After Step 2 complete (Epic Analysis)
3. After each Discovery Loop iteration (Step 3)
4. After Discovery approval (Step 3.4)
5. After feature breakdown approval (Step 4)
6. After epic ticket validation (Step 4.7)
7. After Step 5 complete (Epic Structure Created)
8. After Step 6 complete (S1 done, ready for S2)
9. After session compaction (update "Guide Last Read" with re-read timestamp)

**Agent Status Template:** Include Last Updated, Current Phase, Current Step, Current Guide, Guide Last Read, Critical Rules (3 key rules), Progress, Next Action, Blockers, and Notes.

---

## Prerequisites for S2

**Before transitioning:** Verify all S1 completion criteria met, EPIC_README.md updated for S2, no blockers.

**If prerequisite fails:** Complete missing items before proceeding.

---

## Next Stage

**After completing S1:**

**READ:** `stages/s2/s2_p1_spec_creation_refinement.md` (Spec Creation and Refinement — first of two phases)
**GOAL:** Review Discovery Context, conduct feature-specific research, create spec, resolve checklist, get user approval (Gate 3)
**ESTIMATE:** 2.25-4 hours per feature (3 iterations: I1, I2, I3)

**S2 workflow (split into 2 phases):**
- **S2.P1 (Spec Creation and Refinement):** 3 iterations — I1 (Feature-Level Discovery + Gate 1), I2 (Checklist Resolution), I3 (Refinement & Alignment + Gate 2 + Gate 3)
- **S2.P2 (Cross-Feature Alignment):** Pairwise comparison across all features (Primary agent only)

**Note:** `stages/s2/s2_feature_deep_dive.md` is now a router that links to the 2 phase guides.

**Key Change with Discovery:** S2.P1.I1 now reviews Discovery Context from DISCOVERY.md instead of re-interpreting epic notes. Epic-level understanding is already captured in Discovery.

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S2.P1.

---

*End of stages/s1/s1_epic_planning.md*
