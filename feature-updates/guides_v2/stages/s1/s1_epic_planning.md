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
Epic Planning is the first stage where you create the git branch, analyze the user's epic request, conduct Discovery research, break it down into features, validate your understanding through an epic ticket, and create the folder structure for the entire epic.

**When do you use this guide?**
- User has created `{epic_name}.txt` with their epic request
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

```
+-------------------------------------------------------------+
| CRITICAL RULES - These MUST be copied to README Agent Status |
+-------------------------------------------------------------+

1. CREATE GIT BRANCH BEFORE ANY CHANGES (Step 1.0)
   - Verify on main, pull latest
   - Assign KAI number from EPIC_TRACKER.md
   - Create branch: {work_type}/KAI-{number}
   - Update EPIC_TRACKER.md and commit immediately

2. DISCOVERY PHASE IS MANDATORY (Step 3)
   - Every epic must go through Discovery
   - Cannot create feature folders until Discovery approved
   - Discovery informs feature breakdown
   - See: stages/s1/s1_p3_discovery_phase.md

3. DISCOVERY LOOP UNTIL 3 CONSECUTIVE CLEAN ITERATIONS
   - Continue iterating until 3 consecutive iterations produce no questions
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

7. epic_smoke_test_plan.md is PLACEHOLDER (will update in S4, S8.P2)
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
```

---

## Critical Decisions Summary

**S1 has 5 major decision points. Know these before starting:**

### Decision Point 1: Determine Work Type (Step 1.0d)
**Question:** Is this an epic, feat, or fix?
- **epic:** Work with multiple features (most epics)
- **feat:** Work with single feature only
- **fix:** Bug fix work
- **Impact:** Determines branch name format and EPIC_TRACKER classification

### Decision Point 2: Discovery Loop Exit (Step 3 - S1.P3.2)
**Question:** Have you completed 3 consecutive iterations with no new questions?
- **If NO (counter < 3):** Continue Discovery Loop - re-read with fresh perspective
- **If YES (counter = 3):** Verify exit readiness, proceed to synthesis
- **Impact:** Premature exit (counter < 3) leads to incomplete understanding; need 3 consecutive clean iterations for high confidence

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
+--------------------------------------------------------------+
|                    STAGE 1 WORKFLOW                          |
+--------------------------------------------------------------+

Step 1: Initial Setup
   +-- Create git branch for epic (Step 1.0 - BEFORE any changes)
   |   +-- Verify on main, pull latest
   |   +-- Assign KAI number from EPIC_TRACKER.md
   |   +-- Create branch: {work_type}/KAI-{number}
   |   +-- Update EPIC_TRACKER.md and commit
   +-- Create epic folder
   +-- Move {epic_name}.txt into epic folder
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
   |   +-- Repeat until no new questions
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

## Step 1: Initial Setup

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

### Step 2.4: Update Agent Status

After Step 2:
- Progress: "2/6 steps complete (Epic Analysis)"
- Next Action: "Step 3 - Discovery Phase"

---

## Step 3: Discovery Phase (MANDATORY)

**Goal:** Explore the problem space through iterative research and user Q&A before proposing feature breakdown.

**CRITICAL:** Discovery Phase is MANDATORY for every epic. Cannot create feature folders until Discovery is complete and user-approved.

**Time-Box by Epic Size:**
| Epic Size | Discovery Time |
|-----------|---------------|
| SMALL (1-2 features) | 1-2 hours |
| MEDIUM (3-5 features) | 2-3 hours |
| LARGE (6+ features) | 3-4 hours |

**Detailed Guide:** `stages/s1/s1_p3_discovery_phase.md`

### Discovery Phase Overview

The Discovery Phase is an iterative loop:

```
S1.P3.1: Initialize DISCOVERY.md
    |
    v
S1.P3.2: Discovery Loop
    +-- Research (read code, examine patterns - fresh perspective!)
    +-- Document findings in DISCOVERY.md
    +-- Identify questions
    +-- Ask user, record answers
    +-- Repeat until 3 CONSECUTIVE iterations with NO NEW QUESTIONS
    |
    v
S1.P3.3: Synthesize Findings
    +-- Compare solution options
    +-- Document recommended approach
    +-- Define scope (in/out/deferred)
    +-- Draft feature breakdown
    |
    v
S1.P3.4: User Approval
```

### Key Discovery Outputs

- **DISCOVERY.md** - Epic-level source of truth for decisions
- **Solution approach** - Recommended approach with rationale
- **Scope definition** - What's in, out, and deferred
- **Feature breakdown** - Informed by research and user answers

### Discovery Exit Condition

Discovery Loop exits when 3 CONSECUTIVE research iterations produce NO NEW QUESTIONS. Continue iterating until:
- 3 consecutive iterations with no new unknowns
- All pending questions are resolved
- Scope is clearly defined
- Solution approach is determined
- Clean iteration counter reaches 3

### After Discovery Approval

Once user approves Discovery findings:
1. DISCOVERY.md marked as COMPLETE
2. Proceed to Step 4 (Feature Breakdown Proposal)
3. Feature breakdown is already drafted in DISCOVERY.md

**See full guide:** `stages/s1/s1_p3_discovery_phase.md`

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
2. **Save to:** `feature-updates/{epic_name}/EPIC_TICKET.md`
3. **Present to user** for validation
4. **Proceed to Step 4.7** for user sign-off

**📖 See:** `reference/stage_1/epic_planning_examples.md` → "Example 7: Epic Ticket Template" for:
- Complete epic ticket template
- Guidelines for description, acceptance criteria, success indicators, failure patterns
- Real-world example (Feature 02 epic ticket)

---

### Step 4.7: User Validation of Epic Ticket

**STOP HERE - Do NOT proceed without user validation**

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
   - [x] Epic ticket created and user-validated (Step 4.7)
   ```
2. Epic ticket is now **immutable reference** (like epic notes)
3. Proceed to Step 5

**Critical:** Epic ticket becomes source of truth for outcomes. During Iteration 21 (S5.P3.I3), spec.md will be validated against both epic notes AND epic ticket.

---

## Step 5: Epic Structure Creation

**Prerequisites:**
- User has approved Discovery findings (Step 3)
- User has approved feature breakdown (Step 4)
- User has validated epic ticket (Step 4.7)

### Step 5.1: Create Feature Folders

For EACH approved feature, create folder: `feature-updates/KAI-{N}-{epic_name}/feature_{NN}_{name}/`

**Naming:** Zero-padded numbers + descriptive snake_case name (e.g., `feature_01_adp_integration`)

**For each feature folder, create 4 files:**
1. **README.md** - Use Feature README Template (Agent Status: PLANNING phase)
2. **spec.md** - Seed with Discovery Context section (see below), copy purpose/scope from DISCOVERY.md
3. **checklist.md** - Empty (will populate in S2)
4. **lessons_learned.md** - Template with empty sections

### Step 5.1a: Seed spec.md with Discovery Context

Each feature's spec.md starts with Discovery Context section:

```markdown
# Feature Spec: {feature_name}

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

**IMPORTANT:** Mark this as INITIAL VERSION (placeholder that will be updated in S4 and S8.P2)

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

**Purpose:** Determine which features can start S2 simultaneously vs must wait for dependencies

**For EACH feature, identify:**

1. **Spec Dependencies:**
   - Does this feature need OTHER features' spec.md files to write its own spec?
   - Examples: Tests need argument lists, docs need complete specs, integration layers need interface definitions

2. **Implementation Dependencies:**
   - Does this feature need OTHER features' code to exist before implementation?
   - Examples: Shared utilities, integration components

3. **No Dependencies:**
   - Feature is completely independent
   - Can start S2 immediately

**Create Dependency Matrix:**

Document in EPIC_README.md:

```markdown
## Feature Dependency Groups

**Group 1 (Independent - Round 1):**
- Feature 01: {name}
- Feature 02: {name}
... (list all features with no spec dependencies)

**Group 2 (Depends on Group 1 - Round 2):**
- Feature 08: {name}
  - Depends on: Features 01-07 specs (needs argument lists for test framework)
... (list all features depending on Group 1)

**Group 3 (Depends on Group 2 - Round 3):**
- Feature 09: {name}
  - Depends on: Features 01-08 specs (needs complete scope for documentation)
```

**Workflow with Dependency Groups:**

Each round completes FULL S2→S3→S4 cycle:
- Round 1 (Group 1): S2 (features 1-7) → S3 (validate 1-7) → S4 (test plan with 1-7)
- Round 2 (Group 2): S2 (feature 8) → S3 (validate 8 vs 1-7) → S4 (test plan with 1-8)
- Round 3 (Group 3): S2 (feature 9) → S3 (validate 9 vs 1-8) → S4 (test plan with 1-9)

**Benefits:**
- Dependent features get specs they need before starting S2
- Incremental validation at each round
- Test plan evolves with each round
- No wasted effort on paused/blocked features

**If ALL features are independent:**
```markdown
## Feature Dependency Groups

**All features are independent - Single group (parallel execution)**
```

---

### CHECKPOINT: Parallelization Assessment Gate

**STOP HERE if epic has 2+ features.**

Before proceeding to Step 6 (Transition to S2), you MUST complete Steps 5.8-5.9.

**Checklist:**
- [ ] Feature count verified (if 1 feature, skip to Step 6)
- [ ] If 2+ features: Step 5.8 analysis completed
- [ ] If 3+ features: Step 5.9 offer presented to user
- [ ] User response documented (parallel enabled OR sequential chosen)

**DO NOT proceed to Step 6 until this checkpoint is satisfied.**

---

### Step 5.8: Analyze Features for Parallelization (MANDATORY when 2+ features)

**Purpose:** Determine if S2 parallelization should be offered to user

**MANDATORY:** This step is REQUIRED when the epic has 2+ features. Do NOT skip to Step 6.

**When to analyze:**
- Epic has 2+ features
- Features identified and folder structure created
- Before transitioning to S2

**Analysis Steps:**

1. **Count Features:**
   ```bash
   FEATURE_COUNT=$(ls -d feature_* | wc -l)
   echo "Total features: $FEATURE_COUNT"
   ```

2. **Calculate Potential Savings:**
   ```
   Sequential S2: FEATURE_COUNT × 2 hours = X hours
   Parallel S2: 2 hours (max of all features running simultaneously)
   Savings: X - 2 hours
   ```

   **Examples:**
   - 2 features: Save 2 hours (50% reduction)
   - 3 features: Save 4 hours (67% reduction)
   - 4 features: Save 6 hours (75% reduction)

3. **Analyze Dependencies (Optional for S2):**
   - Read epic request for feature dependencies
   - Note: Dependencies matter for S5-S8 (implementation), NOT for S2 (specs)
   - All features can be researched/specified in parallel regardless of dependencies

4. **Document Assessment:**
   ```markdown
   ## Parallel Work Assessment

   **Total Features:** {N}
   **Parallel S2 Potential:** YES/NO
   **Time Savings (S2):** {X} hours ({Y}% reduction in S2 time)
   **Epic-Level Savings:** {Z} hours ({W}% reduction in total epic time)

   **Recommendation:** OFFER/SKIP parallel work
   ```

**Decision Criteria:**

**OFFER parallel work if:**
- 3+ features (good savings: 4+ hours)
- OR 2 features AND user time-constrained
- OR user specifically requested faster planning

**SKIP parallel work if:**
- Only 1 feature (nothing to parallelize)
- 2 features AND user has time (modest 2-hour savings)
- User prefers simplicity over speed

**If offering parallel work:** Proceed to Step 5.9

**If skipping parallel work:** Skip to Step 6 (standard transition)

### Step 5.9: Offer Parallel Work to User (If Applicable)

**Prerequisites:**
- Analysis shows 2+ features
- Decision made to offer parallelization
- All folders created

**Offering Template:**

```markdown
✅ S1 (Epic Planning) complete!

I've identified {N} features for this epic:
- feature_01: {description} (~2 hours S2)
- feature_02: {description} (~2 hours S2)
- feature_03: {description} (~2 hours S2)

🚀 PARALLEL WORK OPPORTUNITY

I can enable parallel work for S2 (Feature Deep Dives), reducing planning time:

**Sequential approach:**
- Feature 1 S2: 2 hours
- Feature 2 S2: 2 hours
- Feature 3 S2: 2 hours
Total: {sequential_total} hours

**Parallel approach:**
- All {N} features S2: 2 hours (simultaneously)
Total: 2 hours

TIME SAVINGS: {savings} hours ({percent}% reduction in S2 time)

**DEPENDENCIES:**
{dependency_summary}
- All features can be researched/specified in parallel

**COORDINATION:**
- You'll need to open {N-1} additional Claude Code sessions
- I'll coordinate all agents via EPIC_README.md and communication files
- Implementation (S5-S8) remains sequential in this plan

Would you like to:
1. ✅ Enable parallel work for S2 (I'll provide setup instructions)
2. ❌ Continue sequential (I'll do all features one by one)
3. ❓ Discuss parallelization approach
```

**Handle User Response:**

**If Option 1 (Enable parallel work):**
- User will say: "1", "Enable", "Yes to parallel", or similar
- Response: "Great! I'll set up parallel work for S2."
- Skip Step 6 (standard transition)
- **Go to:** `parallel_work/s2_primary_agent_guide.md` Phase 3 (Generate Handoff Packages)
- **Note:** Primary guide includes full parallel workflow through S2→S3→S4
- Return to standard workflow after S4 complete

**If Option 2 (Continue sequential):**
- User will say: "2", "Sequential", "No thanks", or similar
- Response: "Understood. I'll complete features sequentially."
- Proceed to Step 6 (standard transition to S2)

**If Option 3 (Discuss):**
- User will say: "3", "Discuss", "Tell me more", or similar
- Answer questions about:
  - How parallel work functions
  - What user needs to do (open sessions, paste packages)
  - Time savings breakdown
  - Coordination overhead (~10-15% of parallel time)
  - Risk level (LOW - documentation only)
- After discussion: Re-present options 1 and 2
- User chooses Enable or Sequential

**Important Notes:**
- Parallel work offering is **OPTIONAL** (agent decides based on analysis)
- User can always choose sequential (no parallel work forced)
- If user unclear, default to sequential (simpler workflow)
- Parallel work details in: `parallel_work/s2_parallel_protocol.md`

---

## Step 6: Transition to S2

### Step 6.1: Mark S1 Complete

Check all S1 items in EPIC_README.md Epic Completion Checklist.

### Step 6.2: Update Agent Status for S2

Update Agent Status: Current Phase "DEEP_DIVE", Current Guide "stages/s2/s2_p1_research.md", Next Action "Read S2.P1 guide and begin research for feature_01_{name}".

### Step 6.3: Announce Transition to User

Announce S1 completion to user:
- Discovery Phase complete with user approval
- List features created
- List epic-level files created
- Announce transition to S2.P1 (Research Phase) for Feature 1

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

**Why this checkpoint exists:**
- 80% of agents skip re-reading and work from memory
- Discovery Phase is complex and has specific exit conditions
- Missing exit condition causes infinite loops or premature exits

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

**Why this checkpoint exists:**
- Feature breakdown must be grounded in Discovery findings
- 60% of agents skip Discovery context when proposing features
- Missing Discovery context causes misaligned feature scope

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

**Why this checkpoint exists:**
- Epic structure creation has 9 substeps with specific requirements
- 70% of agents miss required files when working from memory
- Missing files cause workflow failures in later stages

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

**Why this checkpoint exists:**
- Epic structure has 15+ required files across epic and feature folders
- 85% of agents miss at least one required file
- Missing files block S2 transition and cause rework

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

**Why this checkpoint exists:**
- S1 completion criteria has 8 mandatory items
- 90% of agents miss at least one item when not re-reading
- Incomplete S1 blocks entire epic workflow

**ONLY after completing ALL 5 actions above, proceed to S2**

---

---

## Completion Criteria

**S1 is complete when ALL of these are true:**

[ ] Git branch created and EPIC_TRACKER.md updated
[ ] DISCOVERY.md created and user-approved
[ ] Epic folder structure complete (EPIC_README, DISCOVERY, test plan, lessons learned, research/, GUIDE_ANCHOR)
[ ] Feature folders created with 4 files each (README, spec with Discovery Context, checklist, lessons learned)
[ ] User approved Discovery findings (Step 3)
[ ] User approved feature breakdown (Step 4)
[ ] User validated epic ticket (Step 4.7)
[ ] Agent Status updated for S2 transition

**If any item unchecked:** Do NOT transition to S2

---

## Common Mistakes to Avoid

```
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
  --> STOP - S1 test plan is placeholder, detailed plan comes in S4

X "I remember the template structure, don't need to check"
  --> STOP - Always use actual template from templates/ folder

X "I'll update Agent Status after I finish all steps"
  --> STOP - Must update after EACH step (not batched)

X "User seems busy, I'll assume they approve"
  --> STOP - Must wait for explicit approval, update Agent Status "Blockers: Waiting for user"

X "I'll skip GUIDE_ANCHOR.md, seems optional"
  --> STOP - GUIDE_ANCHOR.md is MANDATORY (critical for resumption after compaction)

X "The epic_smoke_test_plan.md looks incomplete, let me fill it out"
  --> STOP - It's SUPPOSED to be incomplete (placeholder for S4, S8.P2)

X "I'll number features 1, 2, 3 (no zero-padding)"
  --> STOP - Must use zero-padding: 01, 02, 03 (consistent sorting)

X "I'll skip seeding spec.md with Discovery Context"
  --> STOP - Every spec.md MUST start with Discovery Context section
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

## Guide Comprehension Verification

**Before starting S1, answer these questions:**

1. What must happen before proposing feature breakdown?
   {Answer: Discovery Phase must complete with user approval}

2. When does the Discovery Loop exit?
   {Answer: When a research iteration produces NO new questions}

3. What must happen before creating feature folders?
   {Answer: User must approve Discovery, feature breakdown, AND epic ticket}

4. What section must every feature spec.md start with?
   {Answer: Discovery Context section referencing DISCOVERY.md}

5. Is the epic_smoke_test_plan.md complete after S1?
   {Answer: No, it's a placeholder that updates in S4 and S8.P2}

6. When should you transition to S2?
   {Answer: After ALL Step 6 completion criteria are met and Agent Status updated}

7. What file is the epic-level source of truth for decisions?
   {Answer: DISCOVERY.md}

**Document your answers in EPIC_README.md notes** to prove guide comprehension.

If you cannot answer these questions without re-reading the guide, you haven't read it carefully enough.

---

## Prerequisites for S2

**Before transitioning:** Verify all S1 completion criteria met, EPIC_README.md updated for S2, no blockers.

**If prerequisite fails:** Complete missing items before proceeding.

---

## Next Stage

**After completing S1:**

**READ:** `stages/s2/s2_p1_research.md` (Research Phase - first of three phases)
**GOAL:** Review Discovery Context, conduct feature-specific research, pass research audit
**ESTIMATE:** 45-60 minutes (then continue with S2.P2 and S2.P3)

**S2 workflow (split into 3 phases):**
- **S2.P1 (Research):** Review Discovery Context, feature-specific research, research audit
- **S2.P2 (Specification):** Spec with traceability, alignment check (Steps 2-2.5)
- **S2.P3 (Refinement):** Questions, scope, cross-feature alignment, user approval (Steps 3-6)

**Note:** `stages/s2/s2_feature_deep_dive.md` is now a router that links to the 3 phase guides.

**Key Change with Discovery:** S2.P1 Phase 0 now reviews Discovery Context from DISCOVERY.md instead of re-interpreting epic notes. Epic-level understanding is already captured in Discovery.

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S2.P1.

---

*End of stages/s1/s1_epic_planning.md*
