# S1: Epic Planning Guide

🚨 **MANDATORY READING PROTOCOL**

**Before starting this guide:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update epic EPIC_README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check epic EPIC_README.md Agent Status for current guide
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**What is this guide?**
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
- ✅ Ready to start S2 (feature deep dives)

**Time Estimate:**
45-75 minutes (includes epic ticket validation)

**Exit Condition:**
S1 is complete when you have a validated epic ticket, complete folder structure, and user has confirmed the feature breakdown

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
   - S1: Create structure, propose features
   - S2: Deep dive per feature (separate stage)

10. ⚠️ If unsure about feature breakdown, propose FEWER features
    - Can add features during S2 (discovery)
    - Harder to merge features later

11. ⚠️ Every feature MUST have clear purpose (1-2 sentences)
    - Avoid "miscellaneous" or "utilities" features
    - Each feature delivers distinct value

12. ⚠️ Mark completion in EPIC_README.md before transitioning to S2
```

---

## Critical Decisions Summary

**S1 has 4 major decision points. Know these before starting:**

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
- **Impact:** Epic structure is set - adding features later requires returning to S1

**Note:** Each decision point has clear criteria. Read the detailed section before making decision.

---

## Prerequisites Checklist

**Verify BEFORE starting S1:**

□ User has created `feature-updates/{epic_name}.txt` with epic request notes
□ Epic request file contains sufficient detail (problem description, goals, constraints)
□ No existing epic folder with same name (check `feature-updates/` directory)
□ Git working directory is clean (no uncommitted changes that could conflict)

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with S1
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

Phase 5: Transition to S2
   ├─ Mark S1 complete in EPIC_README.md
   ├─ Update Agent Status (next: S2)
   └─ Announce transition to user
```

---

## Phase 1: Initial Setup

### Step 1.0: Create Git Branch for Epic

**CRITICAL:** Create branch BEFORE making any changes to codebase.

**Steps:**
1. Verify you're on main branch (`git checkout main`)
2. Pull latest changes (`git pull origin main`)
3. Assign KAI number from EPIC_TRACKER.md
4. Determine work type (epic/feat/fix)
5. Create and checkout branch (`git checkout -b {work_type}/KAI-{number}`)
6. Update EPIC_TRACKER.md (add to Active table, increment next number)
7. Commit EPIC_TRACKER.md update immediately

**Why branch first:** Keeps main clean, allows parallel work, enables rollback

---

### Step 1.1: Create Epic Folder

Create epic folder: `feature-updates/KAI-{N}-{epic_name}/`

**Naming:** Use KAI number + snake_case epic name (e.g., `KAI-1-improve_draft_helper`)

### Step 1.2: Move Epic Request File

Move and rename: `{epic_name}.txt` → `KAI-{N}-{epic_name}/{epic_name}_notes.txt`

### Step 1.3: Create EPIC_README.md

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "Epic README Template"

Include Agent Status section with: Current Phase (EPIC_PLANNING), Current Step (Phase 1 complete), Current Guide, Critical Rules, Progress (1/5), Next Action (Phase 2).

### Step 1.4: Update Agent Status

Update Agent Status after Phase 1 completion.

---

## Phase 2: Epic Analysis

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

**📖 See:** `reference/stage_1/feature_breakdown_patterns.md` for:
- Common breakdown patterns (data pipeline, algorithm, multi-source, etc.)
- Decision trees for determining number of features
- Split vs combine decision framework
- Implementation order strategies

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

Present your proposed feature breakdown to the user for approval.

**Include in presentation:**
- Feature list with purpose, scope, dependencies, estimates
- Rationale for breakdown (why this number of features?)
- Recommended implementation order
- Request for user feedback/approval

**📖 See:** `reference/stage_1/epic_planning_examples.md` → "Example 8: Feature Breakdown Presentation" for complete presentation template

### Step 3.4: WAIT for User Approval

⚠️ **STOP HERE - Do NOT proceed without user confirmation**

**DO NOT:**
- ❌ Create feature folders yet
- ❌ Assume user agrees
- ❌ Start S2 deep dives

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

**Process:**

1. **Draft epic ticket** using template from reference guide
2. **Save to:** `feature-updates/{epic_name}/EPIC_TICKET.md`
3. **Present to user** for validation
4. **Proceed to Step 3.7** for user sign-off

**📖 See:** `reference/stage_1/epic_planning_examples.md` → "Example 7: Epic Ticket Template" for:
- Complete epic ticket template
- Guidelines for description, acceptance criteria, success indicators, failure patterns
- Real-world example (Feature 02 epic ticket)

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

**Critical:** Epic ticket becomes source of truth for outcomes. During Iteration 25 (S5.P3.I3), spec.md will be validated against both epic notes AND epic ticket.

---

## Phase 4: Epic Structure Creation

**Prerequisites:**
- User has approved feature breakdown
- User has validated epic ticket

### Step 4.1: Create Feature Folders

For EACH approved feature, create folder: `feature-updates/KAI-{N}-{epic_name}/feature_{NN}_{name}/`

**Naming:** Zero-padded numbers + descriptive snake_case name (e.g., `feature_01_adp_integration`)

**For each feature folder, create 4 files:**
1. **README.md** - Use Feature README Template (Agent Status: PLANNING phase)
2. **spec.md** - Copy purpose/scope/dependencies from Phase 3 proposal (mark as initial)
3. **checklist.md** - Empty (will populate in S2)
4. **lessons_learned.md** - Template with empty sections

### Step 4.2: Create epic_smoke_test_plan.md

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "Epic Smoke Test Plan Template"

**IMPORTANT:** Mark this as INITIAL VERSION (placeholder that will be updated in Stages 4 and 5e)

**Key characteristics of initial version:**
- Based on assumptions from epic request (no implementation knowledge yet)
- Rough guesses for test commands/scenarios
- High-level success criteria (will be refined)
- Marked clearly as "INITIAL - WILL UPDATE"

### Step 4.3: Create epic_lessons_learned.md

Create template file with sections for Planning Phase Lessons, Implementation Phase Lessons, QC Phase Lessons, and Guide Improvements Identified (all empty - will populate during workflow).

### Step 4.4: Create research/ Folder

Create `research/` folder in epic root with README.md explaining purpose (centralizes research/analysis documents, keeps epic root clean).

### Step 4.5: Create GUIDE_ANCHOR.md

Use template from `templates/` folder (see `templates/TEMPLATES_INDEX.md`) → "GUIDE_ANCHOR Template"

**Critical sections:**
- Instructions for resuming after session compaction
- Current stage identification
- Active guide name
- Workflow reference diagram

**This file ensures agents can resume correctly after context window limits.**

### Step 4.6: Update EPIC_README.md

Add **Feature Tracking** table listing all features with S2 Complete and S5.P9 Complete checkboxes (all unchecked initially).

Add **Epic Completion Checklist** with all 7 stages (S1 items checked, all others unchecked).

### Step 4.7: Update Agent Status

Update Agent Status: Progress 4/5, Next Action "Phase 5 - Transition to S2", list features created.

---

## Phase 5: Transition to S2

### Step 5.1: Mark S1 Complete

Check all S1 items in EPIC_README.md Epic Completion Checklist.

### Step 5.2: Update Agent Status for S2

Update Agent Status: Current Phase "DEEP_DIVE", Current Guide "stages/s2/s2_p1_research.md", Next Action "Read S2.P1 guide and begin research for feature_01_{name}".

### Step 5.3: Announce Transition to User

Announce Stage 1 completion to user:
- List features created
- List epic-level files created
- Announce transition to Stage 2a (Research Phase) for Feature 1

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

**S1 is complete when ALL of these are true:**

□ Git branch created and EPIC_TRACKER.md updated
□ Epic folder structure complete (EPIC_README, test plan, lessons learned, research/, GUIDE_ANCHOR)
□ Feature folders created with 4 files each (README, spec, checklist, lessons learned)
□ User approved feature breakdown and epic ticket
□ Agent Status updated for S2 transition

**If any item unchecked:** Do NOT transition to S2

---

## Common Mistakes to Avoid

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll just create the folders, user will probably approve"
   ✅ STOP - Must get explicit approval first

❌ "Let me start the deep dive for Feature 1 while in S1"
   ✅ STOP - S1 only creates structure, S2 does deep dives

❌ "This epic is simple, I'll just make one feature"
   ✅ STOP - Even simple epics benefit from feature breakdown

❌ "I'll create a detailed test plan now"
   ✅ STOP - S1 test plan is placeholder, detailed plan comes in S4

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

**📖 See:** `reference/stage_1/epic_planning_examples.md` for:
- Example 1-4: Real-world feature breakdown examples (good vs bad)
- Example 5: Epic ticket example
- Example 6: Multi-feature epic analysis walkthrough
- Example 7-10: Additional patterns and scenarios

---

## README Agent Status Update Requirements

**Update Agent Status in EPIC_README.md at these points:**

1. ⚡ After Phase 1 complete (Initial Setup)
2. ⚡ After Phase 2 complete (Epic Analysis)
3. ⚡ After Phase 3 proposal presented (mark blocker: waiting for approval)
4. ⚡ After user approves breakdown (clear blocker)
5. ⚡ After Phase 4 complete (Epic Structure Created)
6. ⚡ After Phase 5 complete (S1 done, ready for S2)
7. ⚡ After session compaction (update "Guide Last Read" with re-read timestamp)

**Agent Status Template:** Include Last Updated, Current Phase, Current Step, Current Guide, Guide Last Read, Critical Rules (3 key rules), Progress, Next Action, Blockers, and Notes.

---

## Guide Comprehension Verification

**Before starting S1, answer these questions:**

1. What must happen before creating feature folders?
   {Answer: User must approve feature breakdown}

2. Is the epic_smoke_test_plan.md complete after S1?
   {Answer: No, it's a placeholder that updates in Stages 4 and 5e}

3. How many folders should be created per feature?
   {Answer: One folder per feature with 4 files: README, spec, checklist, lessons_learned}

4. When should you transition to S2?
   {Answer: After ALL Phase 5 completion criteria are met and Agent Status updated}

5. What file ensures agents can resume after session compaction?
   {Answer: GUIDE_ANCHOR.md + EPIC_README.md Agent Status}

**Document your answers in EPIC_README.md notes** to prove guide comprehension.

If you cannot answer these questions without re-reading the guide, you haven't read it carefully enough.

---

## Prerequisites for S2

**Before transitioning:** Verify all S1 completion criteria met, EPIC_README.md updated for S2, no blockers.

**If prerequisite fails:** Complete missing items before proceeding.

---

## Next Stage

**After completing S1:**

📖 **READ:** `stages/s2/s2_p1_research.md` (Research Phase - first of three phases)
🎯 **GOAL:** Extract epic intent, conduct targeted research, pass research audit (Steps 0-1.5)
⏱️ **ESTIMATE:** 45-60 minutes (then continue with S2.P2 and S2.P3)

**S2 workflow (split into 3 phases):**
- **S2.P1 (Research):** Epic intent extraction, targeted research, research audit (Steps 0-1.5)
- **S2.P2 (Specification):** Spec with traceability, alignment check (Steps 2-2.5)
- **S2.P3 (Refinement):** Questions, scope, cross-feature alignment, user approval (Steps 3-6)

**Note:** `stages/s2/s2_feature_deep_dive.md` is now a router that links to the 3 phase guides.

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S2.P1.

---

*End of stages/s1/s1_epic_planning.md*
